var apphost = "http://xing.easy.echosite.cn";
var rurl = apphost + "/register";
var lurl = apphost + "/login";
document.getElementById("submit").onclick = function () {
    $.ajax({
        url: rurl,
        type: 'POST',
        dataType: "JSON",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            "username": $("#user_name").val(),
            "useremail": $("#user_email").val(),
            "phone": $("#phone").val(),
            "password": $("#password").val()
        }),
        success: function (data) {
            console.log(data);
            if (data.flag == 1) {
                alert("注册成功!")
            } else {
                alert(data.errorText);
            }
        },
        error: function (data) {
            alert(data);
        }
    })
}
document.getElementById("button").onclick = function () {
    $.ajax({
        url: lurl,
        type: 'POST',
        dataType: "JSON",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            "username": $("#login_user_name").val(),
            "password": $("#login_password").val()
        }),
        success: function (data) {
            console.log(data);
            if (data.flag == 1) {
                window.localStorage.setItem("username",$("#login_user_name"));
                window.localStorage.setItem("password",$("#login_password"));
                window.location.href = apphost + "/index";
            } else {
                alert(data.errorText);
            }
        },
        error: function (data) {
            alert(data);
        }
    })
}

$(".signin").click(function(){
    this.className="signin focus";
    $(".signup")[0].className="signup";
    $(".input_signin")[0].className="input_signin active";
    $(".input_signup")[0].className="input_signup";
});
$(".signup").click(function(){
    this.className="signup focus";
    $(".signin")[0].className="signin";
    $(".input_signup")[0].className="input_signup active";
    $(".input_signin")[0].className="input_signin";
});