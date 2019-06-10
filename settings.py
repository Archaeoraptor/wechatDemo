RUN = "echosite -config=config.yml start-all"
TOKEN = "123"
APPID = "wx65bbb0c05f89b3af"
APPSECRET = "6152ef56c85bc4eb52f2d28c8ebea0f3"
NULL = ""
WECHATID = "gh_9715d2592755"
URL = "http://xing.easy.echosite.cn"
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
               "url":"http://xing.easy.echosite.cn/main"
            },
            {
               "type":"view",
               "name":"列表",
               "url":"http://xing.easy.echosite.cn/list"
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
           "template_id":"GqFgli7w9_T-h2NKjVX18l5cZGnRiZ_RzMnCWe7lzs8",
           "url":URL +"/list/",
            "data":{
                "first":"推荐文章:",
                "title":"【新闻聚焦】BTV新闻：积极推广防癌健康查体"
            }
       }