#项目相关常量，微信公众号参数配置等
RUN = "echosite -config=config.yml start-all"
TOKEN = "aiyayayi2019"
APPID = "wxa67ed7b1a6dda76f"
APPSECRET = "0d9f94c64b29ee4a164cf996b992d1f6"
NULL = ""
WECHATID = "gh_9add08581213"
#URL = "https://uestc102.cn.utools.club"
#URL = "http://3469396pz2.wicp.vip/"
URL = "https://uestc102.cn.utools.club"
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
               "url":"https://uestc102.cn.utools.club"
            },
            {
               "type":"view",
               "name":"列表",
               "url":"https://uestc102.cn.utools.club"
            },
            {
                 "type":"miniprogram",
                 "name":"万年历",
                 "url":"https://uestc102.cn.utools.club",
                 "appid":"wxb0c4eef8b810664e",
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