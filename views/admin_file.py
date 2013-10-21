# coding: utf-8


import os
import os.path as op
import platform
import shutil
from operator import itemgetter

from werkzeug import secure_filename
from flask import flash, url_for, redirect, request
from flask.ext.admin import helpers
from flask.ext.admin._compat import as_unicode
from flask.ext.admin.base import expose
from flask.ext.admin.babel import gettext
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask.ext.admin.contrib.fileadmin import UploadForm


class PubFile(FileAdmin):
    """酒吧后台文件管理"""

    can_upload = True
    can_delete = True
    can_delete_dirs = False
    can_mkdir = True
    can_rename = False


class PubPicture(FileAdmin):  # todo-lyw代码进一步完善中
    """酒吧图片的后台管理"""
    can_upload = True
    can_delete = True
    can_delete_dirs = False
    can_mkdir = False
    can_rename = False

    allowed_extensions = ('jpg', 'gif', 'png', 'jpeg')

    def __init__(self, base_path, base_url,
                 name=None, category=None, endpoint=None, url=None,
                 verify_path=True):
        """
            Constructor.

            :param base_path:
                Base file storage location
            :param base_url:
                Base URL for the files
            :param name:
                Name of this view. If not provided, will default to the class name.
            :param category:
                View category
            :param endpoint:
                Endpoint name for the view
            :param url:
                URL for view
            :param verify_path:
                Verify if path exists. If set to `True` and path does not exist
                will raise an exception.
        """
        self.base_path = as_unicode(base_path)
        self.base_url = base_url

        self.init_actions()

        self._on_windows = platform.system() == 'Windows'

        # Convert allowed_extensions to set for quick validation
        if (self.allowed_extensions and
            not isinstance(self.allowed_extensions, set)):
            self.allowed_extensions = set(self.allowed_extensions)

        # Convert editable_extensions to set for quick validation
        if (self.editable_extensions and
            not isinstance(self.editable_extensions, set)):
            self.editable_extensions = set(self.editable_extensions)

        # Check if path exists
        if not op.exists(base_path):
            raise IOError('FileAdmin path "%s" does not exist or is not accessible' % base_path)

        super(FileAdmin, self).__init__(name, category, endpoint, url)

    def save_file(self, path, file_data):
        """保存图片"""
        file_data.save(path)

    def on_file_upload(self, directory, path, filename):
        """定义图片上传之后的行为"""
        pass

    def on_file_delete(self, full_path, filename):
        """定义图片删除之后的行为"""
        pass

    @expose('/')
    @expose('/b/<path:path>')
    def index(self, path=None):
        """
            Index view method

            :param path:
                Optional directory path. If not provided, will use the base directory
        """
        # Get path and verify if it is valid
        base_path, directory, path = self._normalize_path(path)

        if not self.is_accessible_path(path):
            flash(gettext(gettext('Permission denied.')))
            return redirect(self._get_dir_url('.index'))

        # Get directory listing
        items = []

        # Parent directory
        if directory != base_path:
            parent_path = op.normpath(op.join(path, '..'))
            if parent_path == '.':
                parent_path = None

            items.append(('..', parent_path, True, 0))

        for f in os.listdir(directory):
            fp = op.join(directory, f)
            rel_path = op.join(path, f)

            if self.is_accessible_path(rel_path):
                items.append((f, rel_path, op.isdir(fp), op.getsize(fp)))

        # Sort by name
        items.sort(key=itemgetter(0))

        # Sort by type
        items.sort(key=itemgetter(2), reverse=True)

        # Generate breadcrumbs
        accumulator = []
        breadcrumbs = []
        for n in path.split(os.sep):
            accumulator.append(n)
            breadcrumbs.append((n, op.join(*accumulator)))

        # Actions
        actions, actions_confirmation = self.get_actions_list()

        return self.render(self.list_template,
                           dir_path=path,
                           breadcrumbs=breadcrumbs,
                           get_dir_url=self._get_dir_url,
                           get_file_url=self._get_file_url,
                           items=items,
                           actions=actions,
                           actions_confirmation=actions_confirmation)

    @expose('/upload/', methods=('GET', 'POST'))
    @expose('/upload/<path:path>', methods=('GET', 'POST'))
    def upload(self, path=None):
        """
            Upload view method

            :param path:
                Optional directory path. If not provided, will use the base directory
        """
        # Get path and verify if it is valid
        base_path, directory, path = self._normalize_path(path)

        if not self.can_upload:
            flash(gettext('File uploading is disabled.'), 'error')
            return redirect(self._get_dir_url('.index', path))

        if not self.is_accessible_path(path):
            flash(gettext(gettext('Permission denied.')))
            return redirect(self._get_dir_url('.index'))

        form = UploadForm(self)
        if helpers.validate_form_on_submit(form):
            filename = op.join(directory,
                               secure_filename(form.upload.data.filename))

            if op.exists(filename):
                flash(gettext('File "%(name)s" already exists.', name=filename),
                      'error')
            else:
                try:
                    self.save_file(filename, form.upload.data)
                    self.on_file_upload(directory, path, filename)
                    return redirect(self._get_dir_url('.index', path))
                except Exception as ex:
                    flash(gettext('Failed to save file: %(error)s', error=ex))

        return self.render(self.upload_template, form=form)

    @expose('/delete/', methods=('POST',))
    def delete(self):
        """
            Delete view method
        """
        path = request.form.get('path')

        if not path:
            return redirect(url_for('.index'))

        # Get path and verify if it is valid
        base_path, full_path, path = self._normalize_path(path)

        return_url = self._get_dir_url('.index', op.dirname(path))

        if not self.can_delete:
            flash(gettext('Deletion is disabled.'))
            return redirect(return_url)

        if not self.is_accessible_path(path):
            flash(gettext(gettext('Permission denied.')))
            return redirect(self._get_dir_url('.index'))

        if op.isdir(full_path):
            if not self.can_delete_dirs:
                flash(gettext('Directory deletion is disabled.'))
                return redirect(return_url)

            try:
                shutil.rmtree(full_path)
                self.on_directory_delete(full_path, path)
                flash(gettext('Directory "%s" was successfully deleted.' % path))
            except Exception as ex:
                flash(gettext('Failed to delete directory: %(error)s', error=ex), 'error')
        else:
            try:
                os.remove(full_path)
                self.on_file_delete(full_path, path)
                flash(gettext('File "%(name)s" was successfully deleted.', name=path))
            except Exception as ex:
                flash(gettext('Failed to delete file: %(name)s', name=ex), 'error')

        return redirect(return_url)