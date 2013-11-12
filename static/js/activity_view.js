// todo-lyw 这个文件应该集成到框架里面去，还有更好的实现方法，目前想不到方案，先ln导入到包里面去了
// 相关的model的create.html和update.html也改变了，需要ln导入

$(document).ready(function(){
    function change_textarea() {
        $("#activity_info").css('width', '552px').css('height', '400px');
    };
    change_textarea();

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

	// 表单屏蔽回车提交
    $("input").keypress(function(e) {
        var keyCode = e.keyCode ? e.keyCode : e.which ? e.which : e.charCode;
        if (keyCode == 13) {
            return false;
        } else {
            return true;
        }
    });

    // 列表页面，如果没有pub_id参数，屏蔽create，如果有更改create的链接，改变cancel的链接
    var pub_id = gup('pub_id')
    if (pub_id) { // 有参数
        var create = $(".nav-tabs li:nth-child(2) a")
        var href = create.attr('href')
        create.attr('href', href+'&pub_id='+pub_id)
        var cancel = $(".control-group .controls a")
        var cancel_href = cancel.attr('href') + '?pub_id=' + pub_id
        cancel.attr('href', cancel_href)
        var edit = $("table tbody a")  // more than on
        for (var i= 0; i < edit.length; i++) {
            var edithref = $(edit[i]).attr('href') + '&pub_id=' + pub_id
            $(edit[i]).attr('href', edithref)
        }
    } else {  // 没有参数
        $(".nav-tabs li:nth-child(2)").remove()
    }
});