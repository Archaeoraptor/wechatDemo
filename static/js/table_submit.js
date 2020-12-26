$("#submit").confirm({
    title: '确定提交吗？',
    content: "<iframe src=\"http://uestc102.cn.utools.club/acknow\"></ifram>",
    confirm: function(){
        console.log("现在跳转到index")
        //window.location.replace(indexurl+"?cc="+document.getElementById("item1").value);
        //window.location.replace(indexurl+"/"+document.getElementById("item1").value);
        $.ajax({
        url: "https://uestc102.cn.utools.club/submit_table",
        type: 'POST',
        dataType: "JSON",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            "username": $("#login_user_name").val(),
            "password": $("#login_password").val(),
            "type": document.getElementById("item1").value
        }),
        success: function (data) {
            if (data.flag == 1) {
                localStorage.setItem("username",$("#login_user_name").val());
                console.log("现在登陆"+$("#login_user_name").val());
                // window.localStorage.setItem("username",$("#login_user_name"));
                // window.localStorage.setItem("password",$("#login_password"));
                window.location.href = root + "/index/"+document.getElementById("item1").value;
            } else {
                console.log(data);
                alert(data.errorText);

            }
        },
        error: function (data) {
            //alert(data);
        }
    })
    },
    cancel: function(){
        $.alert('Canceled!');
    }
    });