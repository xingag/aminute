// 1.新增或者更新一条新闻
$(function () {
    $('#save-news-btn').click(function (event) {
        event.preventDefault();

        var self = $(this);
        //模式对话框
        var news_dialog = $("#news-dialog");
        // 新闻标题
        var title_input = $("input[name='title']");
        // 新闻内容
        var content_input = $("textarea[name='content']");
        // 插图
        var image_input = $("input[name='image_url']");
        // 链接地址
        var link_input = $("input[name='link_url']");
        // 日期
        var current_date_input = $("input[name='current_date']");

        var title = title_input.val();
        var content = content_input.val();
        var image = image_input.val();
        var link = link_input.val();
        var current_date = current_date_input.val();


        //拿到保存按钮绑定的属性：判断此处是新增【Add】，还是更新【Update】
        var submitType = self.attr("data-type");
        var new_id = self.attr("data-id");

        if (!title || !content || !current_date) {
            zlalert.alertInfoToast('请保证数据输入完整');
            return;
        }

        var url = '';
        if (submitType == 'update') {
            url = '/cms/update_news/';
        } else {
            url = '/cms/add_news/';
        }

        //AJAX 发送请求
        zlajax.post({
            'url': url,
            'data': {
                'title': title,
                'content': content,
                'image': image,
                'link': link,
                'current_date': current_date,
                'new_id': new_id
            },
            'success': function (data) {
                news_dialog.modal("hide");
                if (data['code'] == 200) {
                    //重新加载这个页面，获取广告数据
                    window.location.reload();
                } else {
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                console.log(error);
                zlalert.alertNetworkError();
            }
        });
    });
});


// 2.编辑新闻
$(function () {
    $(".edit-news-btn").click(function (event) {
        event.preventDefault();

        var self = $(this);
        var dialog = $("#news-dialog");
        dialog.modal("show");

        //获取tr标签【注意：必须通过tr标签去区分】
        var tr = self.parent().parent();
        //获取tr中绑定的数据
        var title = tr.attr("data-title");
        var content = tr.attr("data-content");
        var img = tr.attr("data-img");
        var link = tr.attr("data-link");
        var current_date = tr.attr("data-current_date");

        //获取控件
        var title_input = dialog.find("input[name='title']")
        var content_input = dialog.find("textarea[name='content']")
        var img_input = dialog.find("input[name='image_url']")
        var link_input = dialog.find("input[name='link_url']")
        var current_date_input = dialog.find("input[name='current_date']")

        //保存按钮
        var saveBtn = dialog.find("#save-news-btn");

        //填充值进去
        title_input.val(title);
        content_input.val(content);
        img_input.val(img);
        link_input.val(link);
        current_date_input.val(current_date);

        //设置按钮的功能为更新【Update】
        saveBtn.attr('data-type', 'update');
        saveBtn.attr('data-id', tr.attr('data-id'))
    });
});


// 3.删除新闻
$(function () {
    $(".delete-news-btn").click(function (event) {
        event.preventDefault();

        var self = $(this);
        var tr = self.parent().parent();
        var news_id = tr.attr('data-id');

        zlalert.alertConfirm({
            "msg": "确定删除这条新闻吗？",
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/cms/delete_news/',
                    'data': {
                        'news_id': news_id
                    },
                    'success': function (data) {
                        if (data['code'] == 200) {
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


//初始化七牛的SDK
$(function () {
    //1.配置七牛云
    zlqiniu.setUp({
        'domain': 'http://pbcomlwfv.bkt.clouddn.com/',   //域名必须加上http和尾部/标签
        'browse_btn': 'upload-btn1',   //点击这个按钮，就可以选择本地图片进行上传到七牛云
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