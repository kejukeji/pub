# coding: utf-8

import logging
import os

from flask.ext.admin.contrib.sqla import ModelView
from flask import flash, request
from flask.ext.admin.babel import gettext
from wtforms.fields import TextAreaField, FileField, TextField
from flask.ext import login

from models import db, Activity
from ex_var import ACTIVITY_PICTURE_BASE_PATH, ACTIVITY_PICTURE_UPLOAD_FOLDER, ACTIVITY_PICTURE_ALLOWED_EXTENSION
from utils import time_file_name, allowed_file_extension, form_to_dict
from werkzeug import secure_filename
from flask.ext.admin.base import expose
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from flask.ext.admin.contrib.sqla import tools

log = logging.getLogger("flask-admin.sqla")


class ActivityView(ModelView):
    """定义活动的视图"""

    page_size = 30
    can_edit = True
    can_delete = True
    can_create = True
    column_display_pk = True
    column_searchable_list = ('title', 'activity_info')
    column_default_sort = ('start_date', True)
    column_labels = dict(
        id=u'ID',
        title=u'活动标题',
        pub_id=u'酒吧ID',
        start_date=u'活动开始时间',
        end_date=u'活动结束时间',
        hot=u'热门活动',
        activity_info=u'活动详情'
    )
    column_exclude_list = ('activity_info', 'base_path', 'rel_path', 'pic_name')

    form_overrides = dict(
        activity_info=TextAreaField
    )

    list_template = 'admin_pub/activity_list.html'
    edit_template = 'admin_pub/activity_edit.html'
    create_template = 'admin_pub/activity_create.html'

    def __init__(self, db, **kwargs):
        super(ActivityView, self).__init__(Activity, db, **kwargs)

    def scaffold_form(self):
        form_class = super(ActivityView, self).scaffold_form()
        form_class.picture = FileField(label=u'酒吧图片', description=u'原来这里可以上传酒吧图片')
        delattr(form_class, 'base_path')
        delattr(form_class, 'rel_path')
        delattr(form_class, 'pic_name')
        return form_class

    def is_accessible(self):
        return login.current_user.is_admin()

    def create_model(self, form):
        """改写flask的新建model的函数"""

        try:
            pub_id = request.args.get('pub_id')
            form._fields['pub_id'] = TextField()
            form._fields['pub_id'].data = int(pub_id)
            model = self.model(**form_to_dict(form))
            self.session.add(model)  # 保存酒吧基本资料
            self.session.commit()
            activity_id = model.id
            activity_pictures = request.files.getlist("picture")  # 获取酒吧图片
            save_activity_pictures(activity_id,activity_pictures)

        except Exception, ex:
            flash(gettext('Failed to create model. %(error)s', error=str(ex)), 'error')
            logging.exception('Failed to create model')
            self.session.rollback()
            return False
        else:
            self.after_model_change(form, model, True)

        return True

    def update_model(self, form, model):
        """改写了update函数"""
        try:
            model.update(**form_to_dict(form))
            self.session.commit()
            activity_id = model.id  # 获取和保存酒吧id
            activity_pictures = request.files.getlist("picture")  # 获取酒吧图片
            save_activity_pictures(activity_id, activity_pictures)
        except Exception, ex:
            flash(gettext('Failed to update model. %(error)s', error=str(ex)), 'error')
            logging.exception('Failed to update model')
            self.session.rollback()
            return False
        else:
            self.after_model_change(form, model, False)

        return True

    def delete_model(self, model):
        """
            Delete model.

            :param model:
                Model to delete
        """
        try:
            self.on_model_delete(model)
            delete_activity_picture(model.id)
            self.session.flush()
            self.session.delete(model)
            self.session.commit()
            return True
        except Exception as ex:
            if self._debug:
                raise

            flash(gettext('Failed to delete model. %(error)s', error=str(ex)), 'error')
            log.exception('Failed to delete model')
            self.session.rollback()
            return False

    def get_list(self, page, sort_column, sort_desc, search, filters, execute=True, pub_id=None):
        """
            Return models from the database.

            :param page:
                Page number
            :param sort_column:
                Sort column name
            :param sort_desc:
                Descending or ascending sort
            :param search:
                Search query
            :param execute:
                Execute query immediately? Default is `True`
            :param filters:
                List of filter tuples
        """

        # Will contain names of joined tables to avoid duplicate joins
        joins = set()

        query = self.get_query()
        count_query = self.get_count_query()

        if pub_id:
            query = query.filter(Activity.pub_id == pub_id)

        # Apply search criteria
        if self._search_supported and search:
            # Apply search-related joins
            if self._search_joins:
                for jn in self._search_joins.values():
                    query = query.join(jn)
                    count_query = count_query.join(jn)

                joins = set(self._search_joins.keys())

            # Apply terms
            terms = search.split(' ')

            for term in terms:
                if not term:
                    continue

                stmt = tools.parse_like_term(term)
                filter_stmt = [c.ilike(stmt) for c in self._search_fields]
                query = query.filter(or_(*filter_stmt))
                count_query = count_query.filter(or_(*filter_stmt))

        # Apply filters
        if filters and self._filters:
            for idx, value in filters:
                flt = self._filters[idx]

                # Figure out joins
                tbl = flt.column.table.name

                join_tables = self._filter_joins.get(tbl, [])

                for table in join_tables:
                    if table.name not in joins:
                        query = query.join(table)
                        count_query = count_query.join(table)
                        joins.add(table.name)

                # Apply filter
                query = flt.apply(query, value)
                count_query = flt.apply(count_query, value)

        # Calculate number of rows
        count = count_query.scalar()

        # Auto join
        for j in self._auto_joins:
            query = query.options(joinedload(j))

        # Sorting
        if sort_column is not None:
            if sort_column in self._sortable_columns:
                sort_field = self._sortable_columns[sort_column]

                query, joins = self._order_by(query, joins, sort_field, sort_desc)
        else:
            order = self._get_default_order()

            if order:
                query, joins = self._order_by(query, joins, order[0], order[1])

        # Pagination
        if page is not None:
            query = query.offset(page * self.page_size)

        query = query.limit(self.page_size)

        # Execute if needed
        if execute:
            query = query.all()

        return count, query

    # Views
    @expose('/')
    def index_view(self):
        """
            List view
        """
        pub_id = request.args.get('pub_id', None)
        if pub_id:
            pub_id = int(pub_id)

        # Grab parameters from URL
        page, sort_idx, sort_desc, search, filters = self._get_extra_args()

        # Map column index to column name
        sort_column = self._get_column_by_idx(sort_idx)
        if sort_column is not None:
            sort_column = sort_column[0]

        # Get count and data
        count, data = self.get_list(page, sort_column, sort_desc,
                                    search, filters, pub_id=pub_id)  # 改写了函数，根据pub_id过滤

        # Calculate number of pages
        num_pages = count // self.page_size
        if count % self.page_size != 0:
            num_pages += 1

        # Pregenerate filters
        if self._filters:
            filters_data = dict()

            for idx, f in enumerate(self._filters):
                flt_data = f.get_options(self)

                if flt_data:
                    filters_data[idx] = flt_data
        else:
            filters_data = None

        # Various URL generation helpers
        def pager_url(p):
            # Do not add page number if it is first page
            if p == 0:
                p = None

            return self._get_url('.index_view', p, sort_idx, sort_desc,
                                 search, filters)

        def sort_url(column, invert=False):
            desc = None

            if invert and not sort_desc:
                desc = 1

            return self._get_url('.index_view', page, column, desc,
                                 search, filters)

        # Actions
        actions, actions_confirmation = self.get_actions_list()

        return self.render(self.list_template,
                               data=data,
                               # List
                               list_columns=self._list_columns,
                               sortable_columns=self._sortable_columns,
                               # Stuff
                               enumerate=enumerate,
                               get_pk_value=self.get_pk_value,
                               get_value=self.get_list_value,
                               return_url=self._get_url('.index_view',
                                                        page,
                                                        sort_idx,
                                                        sort_desc,
                                                        search,
                                                        filters),
                               # Pagination
                               count=count,
                               pager_url=pager_url,
                               num_pages=num_pages,
                               page=page,
                               # Sorting
                               sort_column=sort_idx,
                               sort_desc=sort_desc,
                               sort_url=sort_url,
                               # Search
                               search_supported=self._search_supported,
                               clear_search_url=self._get_url('.index_view',
                                                              None,
                                                              sort_idx,
                                                              sort_desc),
                               search=search,
                               # Filters
                               filters=self._filters,
                               filter_groups=self._filter_groups,
                               filter_types=self._filter_types,
                               filter_data=filters_data,
                               active_filters=filters,

                               # Actions
                               actions=actions,
                               actions_confirmation=actions_confirmation)


def save_activity_pictures(activity_id, pictures):
    """保存酒吧图片"""
    for picture in pictures:
        if not allowed_file_extension(picture.filename, ACTIVITY_PICTURE_ALLOWED_EXTENSION):
            continue
        else:
            upload_name = picture.filename
            base_path = ACTIVITY_PICTURE_BASE_PATH
            rel_path = ACTIVITY_PICTURE_UPLOAD_FOLDER
            pic_name = time_file_name(secure_filename(upload_name), sign=activity_id)
            activity = Activity.query.filter(Activity.id == activity_id).first()
            if activity:
                old_picture = str(activity.base_path) + str(activity.rel_path) + '/' + str(activity.pic_name)
                picture.save(os.path.join(base_path+rel_path+'/', pic_name))
                activity.pic_name = pic_name
                activity.base_path = base_path
                activity.rel_path = rel_path
                db.commit()
                try:
                    os.remove(old_picture)
                except OSError:
                    message = "Error while os.remove on %s" % str(picture)
                    flash(message, 'error')


def delete_activity_picture(activity_id):
    activity = Activity.query.filter(Activity.id == activity_id).first()
    if activity:
        picture = str(activity.base_path) + str(activity.rel_path) + '/' + str(activity.pic_name)

        try:
            os.remove(picture)
        except OSError:
            message = "Error while os.remove on %s" % str(picture)
            flash(message, 'error')