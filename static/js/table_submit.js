$("#submit").confirm({
    title: '确定提交吗？',
    content: "<iframe style='width:98%' src=\"https://uestctest.cn1.utools.club/acknow\"></iframe>",
    confirm: function(){
        console.log("现在跳转到index")
        //window.location.replace(indexurl+"?cc="+document.getElementById("item1").value);
        //window.location.replace(indexurl+"/"+document.getElementById("item1").value);
        var treatment="";
        $('input[name="category"]').each(function(){
            if($(this).prop("checked")){
                treatment = treatment.concat($(this).attr('value')," ");
            }
        });
        treatment = treatment.concat($('input[name="category_else"]').val());
        var retreatment="";
        $("input[name='category_retreatment']:checked").each(function(i){
            retreatment = retreatment.concat($(this).attr("value")," ") ;
        });
        var channel="";
        $('input[name="category_channel"]').each(function(){
            if($(this).prop("checked")){
                channel = channel.concat($(this).attr('value')," ");
            }
        });
        channel = channel.concat($('input[name="category_channel_else"]').val());
        var interest="";
        $('input[name="category_interest"]').each(function(){
            if($(this).prop("checked")){
                interest=interest.concat($(this).attr('value')," ");
            }
        });
        interest=interest.concat($('input[name="category_interest_else"]').val());
        var method="";
        $("input[name='category_method']:checked").each(function(i){
            method = $(this).attr("value");
        });
        method += $('input[name="category_method_else"]').val();
        var frequency="";
        $("input[name='category_frequency']:checked").each(function(i){
            frequency = $(this).attr("value");
        });
        frequency += $('input[name="category_frequency_else"]').val();
        //alert(treatment+'|'+channel+'|'+interest+'|'+method+'|'+frequency);
        $.ajax({
        url: "https://uestctest.cn1.utools.club/submit_table",
        type: 'POST',
        dataType: "JSON",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            "username": $("#login_user_name").val(),
            "password": $("#login_password").val(),
            "type": document.getElementById("item1").value,
            "year": $("#item2").val(),
            "treatment": treatment,
            "institude": $("#item2_1").val(),
            "retreatment": retreatment,
            "channel": channel,
            "interest": interest,
            "method": method,
            "frequency": frequency,
        }),
        traditional: true,
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