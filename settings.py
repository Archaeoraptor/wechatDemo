TOKEN = "123"
# APPID = "wx65bbb0c05f89b3af"
# APPSECRET = "6152ef56c85bc4eb52f2d28c8ebea0f3"
APPID = "wx69b71a53ddecce39"
APPSECRET = "98ef3811227471523d01f1b5e0e1ad12"
NULL = ""
MENU =  {
     "button":[
     {
          "type":"click",
          "name":"今日歌曲",
          "key":"V1001_TODAY_MUSIC"
      },
      {
           "name":"菜单",
           "sub_button":[
           {
               "type":"view",
               "name":"搜索",
               "url":"https://mp.weixin.qq.com/mp/subscribemsg?action=get_confirm&appid=wxaba38c7f163da69b&scene=1000&template_id=1uDxHNXwYQfBmXOfPJcjAS3FynHArD8aWMEFNRGSbCc&redirect_url=http%3a%2f%2fsupport.qq.com&reserved=test#wechat_redirect"
            },
            {
               "type":"view",
               "name":"列表",
               "url":"http://panghu.ngrok.xiaomiqiu.cn/list/"
            },
            {
                 "type":"miniprogram",
                 "name":"wxa",
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
           "touser":"oIPLH1PpcmFfP3SEnH2PZ9fAA-Tk",
           "template_id":"B4oBg0f2ocIm0hMt--7SNswCGJlypWccZycQ5X8Twqc",
           "url":"http://panghu.ngrok.xiaomiqiu.cn/list/",
       }