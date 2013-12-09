$(document).ready(function(){
    // 定义获取当前url属性的函数
    function gup( name ) {
        name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
        var regexS = "[\\?&]"+name+"=([^&#]*)";
        var regex = new RegExp( regexS );
        var results = regex.exec( window.location.href );
        if( results == null )
            return "";
        else
            return results[1];
    }

    function initUpload() {
        var pub_id = gup('pub_id');
        var activity_id = gup('activity_id');
        $("div:contains('With selected')").last().remove();
        if (pub_id) {
            $("a[href='/admin/pubpicturefile/upload/']").attr('href',
                "/admin/pubpicturefile/upload?pub_id="+gup('pub_id'));
        }
        if (activity_id) {
            $("a[href='/admin/activitypicturefile/upload/']").attr('href',
                "/admin/activitypicturefile/upload?activity_id="+gup('activity_id'));
        }
    }

    initUpload();
});