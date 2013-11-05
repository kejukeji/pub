// todo-lyw 这个文件应该集成到框架里面去，还有更好的实现方法，目前想不到方案，先ln导入到包里面去了
// 相关的model的create.html和update.html也改变了，需要ln导入

$(document).ready(function(){
	function add_select() {
		g_city_id = $("#city_id").val();
		g_province_id = $("#province_id").val();
		g_county_id = $("#county_id").val();
		var city_select = $.parseHTML("<select name='city_id' id='city_id'></select>");
		$("#city_id").replaceWith(city_select);
		var county_select = $.parseHTML("<select name='county_id' id='county_id'></select>");
		$("#county_id").replaceWith(county_select);
		var province_select = $.parseHTML("<select name='province_id' id='province_id'></select>");
		$("#province_id").replaceWith(province_select);
		// 添加文件上传
		var picture_select = $.parseHTML("<input class='btn btn-success' type='file' name='picture' id='picture' multiple>");
		$("#picture").replaceWith(picture_select);
		// 添加百度地图
		$("#latitude").parent().parent().parent().after("<div id='baidumap' style='width:800px; height:500px; margin-bottom:20px;'></div>");
		// 添加地图搜索
		$("#latitude").parent().parent().parent().after("<div id='float_search_bar'><input type='text' id='keyword' /><span id='search_button' style='margin-left:-45px;' class='btn'>查找</span></div>");
	};

	add_select();

    function change_textarea() {
        $("#intro").css('width', '552px').css('height', '400px');
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

    function init_loacation(init_province, init_city, init_county) {
        // 获取省的json
        $.ajax({
            type: "GET",
            url: "/restful/admin/province",
            dataType: "json",
            async: false,
            cache: false,
            success: function(json) {
                $("#province_id").empty();
                $.each(json, function(i, value) {
                    $("#province_id").append($("<option>").text(value[1]).attr('value', value[0]));
                });
                $("#province_id").val(init_province);
            },
            error: function() {
                alert("获取省份资料失败，请刷新网页！");
            }
        });

        // 获取特定省下面的市区
        $.ajax({
            type: "GET",
            url: "/restful/admin/city/" + init_province,
            dataType: "json",
            async: false,
            cache: false,
            success: function(json) {
                $("#city_id").empty();
                $.each(json, function(i, value) {
                    $("#city_id").append($("<option>").text(value[1]).attr('value', value[0]));
                });
                $("#city_id").val(init_city);
                // 这里设置市改变之后，区县的option也跟着改变
            },
            error: function() {
                alert("获取市资料失败，请刷新网页！");
            }
        });

        // 获取特定市下面的区县
        $.ajax({
            type: "GET",
            url: "/restful/admin/county/" + init_city,
            dataType: "json",
            async: false,
            cache: false,
            success: function(json) {
                $("#county_id").empty();
                $.each(json, function(i, value) {
                    $("#county_id").append($("<option>").text(value[1]).attr('value', value[0]));
                });
                $("#county_id").val(init_county);
            },
            error: function() {
                alert("获取区县资料失败，请刷新页面！")
            }
        })
    };

    // 如果是新建的话，这几个id是不存在的，无法获取，使用默认参数
    if (g_province_id != "") {
        init_loacation(g_province_id, g_city_id, g_county_id);
    } else {
        init_loacation(9, 75, 794);
    }

    // 如果不是新建的话，添加一个图片管理的东西，到哪里去
    if (g_province_id != "") {
        var manager_link = $.parseHTML("<p><a class='btn btn-danger' href='/admin/pubpicturefile?pub_id="+gup('id')+"'>图片管理</a></p>");
        $("#picture").after(manager_link)
        $("#picture").remove()  // 去掉图片上传
    }

	$("select").change(function() {
		if (g_province_id != $("#province_id").val()) {
			province_change();
			return true;
		}
		if (g_city_id != $("#city_id").val()) {
			city_change();
			return true;
		}
	});

	function province_change() {
		g_province_id = $("#province_id").val();

	    // 获取特定省下面的市区
	    $.ajax({
	         type: "GET",
	         url: "/restful/admin/city/" + g_province_id,
	         dataType: "json",
	         async: false,
	         cache: false,
	         success: function(json) {
	             $("#city_id").empty();
	             $.each(json, function(i, value) {
	                 $("#city_id").append($("<option>").text(value[1]).attr('value', value[0]));
	             });
	         },
	         error: function() {
	             alert("获取市资料失败，请刷新网页！");
	         }
	    });

	    g_city_id = $("#city_id").val()

	    $.ajax({
	         type: "GET",
	         url: "/restful/admin/county/" + g_city_id,
	         dataType: "json",
	         async: false,
	         cache: false,
	         success: function(json) {
	             $("#county_id").empty();
	             $.each(json, function(i, value) {
	                 $("#county_id").append($("<option>").text(value[1]).attr('value', value[0]));
	             });
	         },
	         error: function() {
	             alert("获取区县资料失败，请刷新网页！");
	         }
	    });

	    g_county_id = $("#county_id").val();
   	    //p6(g_province_id, g_city_id, g_county_id, $("#province_id").val(), $("#city_id").val(), $("#county_id").val());
	};

	function city_change() {
		g_city_id = $("#city_id").val();

	     // 获取特定市下面的区县
	    $.ajax({
	         type: "GET",
	         url: "/restful/admin/county/" + g_city_id,
	         dataType: "json",
	         async: false,
	         cache: false,
	         success: function(json) {
	             $("#county_id").empty();
	             $.each(json, function(i, value) {
	                 $("#county_id").append($("<option>").text(value[1]).attr('value', value[0]));
	             });
	         },
	         error: function() {
	             alert("获取区县资料失败，请刷新网页！");
	         }
	    });

	    g_county_id = $("#county_id").val();
	};

	function p6(a1, a2, a3, a4, a5, a6) {
		alert("p+"+a1+"  c+"+a2+"  co+"+a3+"  p+"+a4+"  c+"+a4+"  co+"+a6);
	};

    function getPubType() {
        var pub_type = ""
        var id = gup("id"); // returns "7"

        if (id) {
            $.ajax({
                type: "GET",
                url: "/restful/admin/pub_type_list/" + id,
                dataType: "json",
                async: false,
                cache: false,
                success: function(json) {
                    $.each(json, function(i, value) {
                        pub_type = value;
                    });
                },
                error: function() {
                    alert("获取酒吧类型失败，请刷新页面！")
                }
            });
        }

        return pub_type.split(","); // ['1', '2']
    }

	// 获取酒吧类型
	$.ajax({
		type: "GET",
		url: "/restful/admin/pub_type",
		dataType: "json",
		async: false,
		cache: false,
		success: function(json) {
			var pub_type_select = $.parseHTML("<select multiple name='pub_type' id='pub_type'></select>");
			$("#pub_type").replaceWith(pub_type_select);
			$.each(json, function(i, value) {
				$("#pub_type").append($('<option>').text(value[1]).attr('value', value[0]));
			});
            $("#pub_type").val(getPubType());
			$("#pub_type").select2({
				width: '220px'
			});
		},
		error: function() {
			alert("获取酒吧类型资料失败，请刷新网页！");
		}
	});

	// 地图初始化
	function setResult(lng, lat) {
		$("#latitude").val(lat);
		$("#longitude").val(lng);
	};

	function init_map() {
		createMap();
		setMapEvent(); // 设置地图事件
		addMapControl(); // 向地图添加控件
	};

	function createMap() {
		var map = new BMap.Map("baidumap"); //在百度地图容器中创建一个地图
		var point = new BMap.Point(121.487899, 31.249162);
		map.centerAndZoom(point, 12);
		window.map = map; //将map变量存储在全局
	};

	function setMapEvent() {
        map.enableDragging(); //启用地图拖拽事件，默认启用(可不写)
        map.enableScrollWheelZoom(); //启用地图滚轮放大缩小
        map.enableDoubleClickZoom(); //启用鼠标双击放大，默认启用(可不写)
        map.enableKeyboard(); //启用键盘上下左右键移动地图
	};

	function addMapControl() {
        //向地图中添加缩放控件
		var ctrl_nav = new BMap.NavigationControl({anchor:BMAP_ANCHOR_TOP_LEFT,type:BMAP_NAVIGATION_CONTROL_SMALL});
		map.addControl(ctrl_nav);
        //向地图中添加缩略图控件
		var ctrl_ove = new BMap.OverviewMapControl({anchor:BMAP_ANCHOR_BOTTOM_RIGHT,isOpen:0});
		map.addControl(ctrl_ove);
        //向地图中添加比例尺控件
		var ctrl_sca = new BMap.ScaleControl({anchor:BMAP_ANCHOR_BOTTOM_LEFT});
		map.addControl(ctrl_sca);
	};

	init_map();

// 百度地图数据部分 start
	var marker_trick = true;
	var marker = new BMap.Marker(new BMap.Point(121.487899, 31.249162), {
		enableMassClear: false,
		raiseOnDrag: true
	});
	marker.enableDragging();
	map.addEventListener("click", function(e) {
		setResult(e.point.lng, e.point.lat);
	});
	marker.addEventListener("dragend", function(e) {
		setResult(e.point.lng, e.point.lat);
	});
	var local = new BMap.LocalSearch(map, {
		renderOptions: {map: map},
		pageCapacity: 1
	});
	local.setSearchCompleteCallback(function(results) {
		if (local.getStatus() != BMAP_STATUS_SUCCESS) {
			alert("无结果");
		} else {
			marker.hide();
		}
	});
	local.setMarkersSetCallback(function(pois) {
		for (var i=pois.length; i--; ) {
			var marker = pois[i].marker;
			marker.addEventListener("click", function(e) {
				marker_trick = True;
				var pos = this.getPosition();
				setResult(pos.lng, pos.lat);
			});
		}
	});
    $("#keyword").change(function() {
    	local.search($("#keyword").val());
    });
    $("#keyword").onkeyup = function(e){
        var me = this;
        e = e || window.event;
        var keycode = e.keyCode;
        if(keycode === 13){
            local.search($("#keyword").val());
        }
    };
// 百度地图数据部分 stop

	//填写酒吧名字自动填写搜索的内容
	$("#name").change(function() {
		$("#keyword").val($("#name").val());
    	local.search($("#keyword").val());
	})

	// 表单屏蔽回车提交
    $("input").keypress(function(e) {
        var keyCode = e.keyCode ? e.keyCode : e.which ? e.which : e.charCode;
        if (keyCode == 13) {
            return false;
        } else {
            return true;
        }
    });

	// 多选的时候返回1，2，3
	$("input[value|='Submit']").click(function() {
		var pub_type = $("#pub_type").val().toString();
		var pub_type_text = $.parseHTML("<input id='pub_type' tpye='text' name='pub_type'>")
		$("#pub_type").replaceWith(pub_type_text)
		$("#pub_type").val(pub_type)
	});
});