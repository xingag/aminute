//管理轮播图

$(function () {

    //新增【更新】一条轮播图
    $("#save-banner-btn").click(function (event) {
        event.preventDefault();

        //拿到自己
        var self = $(this);

        //先查找对话框的div，然后再使用jquery查找子元素
        var dialog = $("#banner-dialog");
        var image_input = $("input[name='image_url']");
        var current_date_input = $("input[name='current_date']");

        var image = image_input.val();
        var current_date = current_date_input.val();

        //拿到保存按钮中存放的属性值【是保存还是更新】
        var submitType = self.attr("data-type");
        var bannerId = self.attr("data-id");


        //输入为空的时候，直接返回
        if ( !image || !current_date) {
            zlalert.alertInfoToast('请保证数据输入完整');
            return;
        }

        var url = '';
        //判断是保存功能还是更新功能
        if (submitType == 'update') {
            url = '/cms/update_banner/';
        } else {
            url = '/cms/add_banner/';
        }


        //输入如果输入正确，就用ajax发送给服务器
        zlajax.post({
            "url": url,
            "data": {
                "image": image,
                "current_date": current_date,
                "banner_id": bannerId
            },
            "success": function (data) {
                //隐藏对话框【bootcss】
                dialog.modal("hide");
                if (data['code'] == 200) {
                    //重新加载这个页面，获取广告数据
                    window.location.reload();
                } else {
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError();
            }
        });

    });
});


//关闭模态对话框的监听事件 - close-banner-btn
$(function () {
    $("#close-banner-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);

        var dialog = $("#banner-dialog");

        var image_input = dialog.find("input[name='image_url']");
        // var date_input = dialog.find("input[name='current_date']");

        //清空数据
        image_input.val('');
        // date_input.val('');

    });

});


//编辑按钮的监听事件
$(function () {

    $(".edit-banner-btn").click(function (event) {
        event.preventDefault();

        //自己
        var self = $(this);

        // 1.弹出轮播图编辑的对话框
        // 2.带该条记录的内容
        var dialog = $("#banner-dialog");

        // 3.显示对话框
        dialog.modal("show");

        // 4.通过【编辑】按钮得到tr标签，进而得到绑定到上面的数据
        var tr = self.parent().parent();

        // 5.获取到tr标签上绑定的数据
        var image = tr.attr("data-image");
        var current_date = tr.attr("data-date");


        // 6.2【第二种方式：从dialog中去获取，效率更高一些】
        var image_input = dialog.find("input[name='image_url']");
        var date_input = dialog.find("input[name='current_date']");
        var saveBtn = dialog.find("#save-banner-btn");

        // 7.把值设置到input标签中去
        image_input.val(image);
        date_input.val(current_date);

        // 8.给保存按钮绑定一个属性【代表是更新】
        saveBtn.attr('data-type', 'update');
        saveBtn.attr('data-id', tr.attr('data-id'))

    });

});


//删除轮播图的点击事件
$(function () {
    $(".delete-banner-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);

        // 1.获取到tr标签
        var tr = self.parent().parent();

        // 2.获取banner_id
        var banner_id = tr.attr('data-id');

        // 3.弹出对话框，让用户自己去选择是否删除这条轮播图数据
        zlalert.alertConfirm({
            "msg": "确定删除轮播图？",
            'confirmCallback': function () {
                // 2.利用ajax发送删除请求
                zlajax.post({
                    'url': '/cms/delete_banner/',
                    'data': {
                        'banner_id': banner_id
                    },
                    'success': function (data) {
                        if (data['code'] == 200) {
                            //删除成功之后，重新加载这个页面
                            window.location.reload();
                        } else {
                            zlalert.alertInfo(data['message']);
                        }
                    },
                    'fail': function (error) {
                        zlalert.alertNetworkError();
                    }
                });
            }
        });


    });
});


//初始化七牛的SDK
$(function () {
    //1.配置七牛云
    zlqiniu.setUp({
        'domain': 'http://pbcomlwfv.bkt.clouddn.com/',   //域名必须加上http和尾部/标签
        'browse_btn': 'upload-btn',   //点击这个按钮，就可以选择本地图片进行上传到七牛云
        'uptoken_url': '/c/uptoken/',

        //2.上传完成之后的正确回调
        'success': function (up, file, info) {
            console.log(file);
            //3.获取输入框,并把图片上传后的地址设置到输入框内
            var imageInput = $("input[name='image_url']");
            imageInput.val(file.name);


        }
    });
});