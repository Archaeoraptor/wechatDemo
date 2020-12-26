document.getElementById("submit").onclick = function () {
        $.ajax({
        url: logout,
        type: 'POST',
        dataType: "JSON",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            // "username": $("#user_name").val(),
            // "password": $("#password").val(),
            "user_id": localStorage.getItem("user_id"),
        }),
        success: function (data) {
            console.log(data);
            if (data.flag == 1) {
                alert("退出登录成功!");
                window.location.href = root + "/logout";
            } else {
                alert(data.errorText);
            }
        },
        error: function (data) {
            alert(data);
        }
    })
}