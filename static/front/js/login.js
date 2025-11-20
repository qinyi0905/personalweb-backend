var LoginHandler = function () {

}

LoginHandler.prototype.listenGraphCaptchaEvent = function () {
    $("#captcha-img").on("click", function () {
        var $this = $(this);
        var src = $this.attr("src");
        let new_src = zlparam.setParam(src, "sign", Math.random())
        $this.attr("src", new_src);
    });
}

LoginHandler.prototype.listenSubmitEvent = function () {
    $("#btn-login").on("click", function (event) {
        event.preventDefault();
        var username = $("input[name='username']").val();
        var password = $("input[name='password']").val();
        var graph_captcha = $("input[name='graph-captcha']").val();

        zlajax.post({
            url: "/login",
            data: {
                "username": username,
                "password": password,
                "graph_captcha": graph_captcha
            },
            success: function (result) {
                if (result['code'] == 200) {
                    var token = result['data']['token'];
                    var user = result['data']['user'];
                    localStorage.setItem("JWT_TOKEN_KEY", token);
                    localStorage.setItem("USER_KEY", JSON.stringify(user));
                    window.location="/cms";
//                    window.location="http://127.0.0.1:8080"
                } else {
                    alert(result['message']);
                }
            }
        })
    });
}


LoginHandler.prototype.run = function () {
    this.listenGraphCaptchaEvent();
    this.listenSubmitEvent();
}

// $(function(){})
$(function () {
    var handler = new LoginHandler();
    handler.run();
});