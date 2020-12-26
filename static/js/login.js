document.getElementById("submit").onclick = function () {
        $.ajax({
        url: rurl,
        type: 'POST',
        dataType: "JSON",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            "username": $("#user_name").val(),
            "password": $("#password").val(),
        }),
        success: function (data) {
            console.log(data);
            if (data.flag == 1) {
                alert("注册成功!");
                $(".signin").click();
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
            "password": $("#login_password").val(),
        }),
        success: function (data) {
            if (data.flag == 1) {
                if(data.cancer_type == null || data.cancer_type == ''){
                    localStorage.setItem("username",$("#login_user_name").val());
                    console.log("现在登陆"+$("#login_user_name").val());
                    // window.localStorage.setItem("username",$("#login_user_name"));
                    // window.localStorage.setItem("password",$("#login_password"));
                    window.location.href = root + "/table";
                }else{
                    window.location.href = root + "/index/"+data.cancer_type;
                }
            } else {
                console.log(data);
                alert(data.errorText);

            }
        },
        error: function (data) {
            //alert(data);
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