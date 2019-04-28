TOKEN = "123"
APPID = "wx65bbb0c05f89b3af"
APPSECRET = "6152ef56c85bc4eb52f2d28c8ebea0f3"
NULL = ""
MENU =  {
     "button":[
     {
          "type":"click",
          "name":"个人信息",
          "key":"V1001_TODAY_MUSIC"
      },
      {
           "name":"菜单",
           "sub_button":[
           {
               "type":"view",
               "name":"搜索",
               "url":"https://www.baidu.com"
            },
            {
               "type":"view",
               "name":"列表",
               "url":"http://panghu.ngrok.xiaomiqiu.cn/list/"
            },
            {
                 "type":"miniprogram",
                 "name":"万年历",
                 "url":"http://mp.weixin.qq.com",
                 "appid":"wx286b93c14bbf93aa",
                 "pagepath":"pages/lunar/index"
             },
            {
               "type":"click",
               "name":"赞一下我们",
               "key":"V1001_GOOD"
            }]
       }]
 }
TEMPLATE_MSG = {
           "touser":"oIPLH1P31seTfvqU2Gvr852DHS_Q",
           "template_id":"B4oBg0f2ocIm0hMt--7SNswCGJlypWccZycQ5X8Twqc",
           "url":"http://panghu.ngrok.xiaomiqiu.cn/list/",
       }