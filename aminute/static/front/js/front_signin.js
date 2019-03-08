$(function () {
    $("#submit-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);

        var telephone_input = $("input[name='telephone']");
        var password_input = $("input[name='password']");
        var remember_input = $("input[name='remember']");

        var telephone = telephone_input.val();
        var password = password_input.val();
        //选择了就赋值为1，否则为0
        var remember = remember_input.checked ? 1 : 0;

        zlajax.post({
            'url': '/signin/',
            'data': {
                'telephone': telephone,
                'password': password,
                'remember': remember
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
                    zlalert.alertInfo(data['message'])
                }
            },
            'fail': function (error) {
                console.log(error);
            }
        });

    });
});