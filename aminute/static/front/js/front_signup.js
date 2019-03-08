$(function () {
    $("#submit-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);

        var telephone_input = $("input[name='telephone']");
        var username_input = $("input[name='username']");
        var password1_input = $("input[name='password1']");
        var password2_input = $("input[name='password2']");

        var telephone = telephone_input.val();
        var username = username_input.val();
        var password1 = password1_input.val();
        var password2 = password2_input.val();


        //把数据通过ajax提交给后台
        zlajax.post({
            'url': '/signup/',
            'data': {
                'telephone': telephone,
                'username': username,
                'password1': password1,
                'password2': password2
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    var return_to = $("#return-to-span").text();
                    if (return_to) {
                        window.location = return_to;
                    } else {
                        window.location = '/';
                    }
                } else {
                    zlalert.alertErrorToast(data['message']);
                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError();
            }

        });


    });
});