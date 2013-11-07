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
});