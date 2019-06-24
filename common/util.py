#通用工具，暂未分类管理
import requests
import json
from settings import TOKEN, MENU, TEMPLATE_MSG, NULL, URL
import xml.etree.ElementTree as ET
import hashlib
from models.WechatToken import AccessToken


def validate_wx_public(form, token=TOKEN):
    timestamp = form.timestamp.data
    nonce = form.nonce.data
    echostr = form.echostr.data
    signature = form.signature.data
    array = [timestamp, nonce, TOKEN]
    array.sort()
    arr_to_str = "".join(array)
    result = hashlib.sha1(arr_to_str.encode("utf-8")).hexdigest()
    return result == signature, echostr


def parseXML(str):
    root = ET.fromstring(str)
    result = []
    for el in root:
        if el.tag == "FromUserName":
            result.append(el.text)
        if el.tag == "Content":
            result.append(el.text)
    return result

def createXML():
    """
    <xml>
      <ToUserName><![CDATA[toUser]]></ToUserName>
      <FromUserName><![CDATA[fromUser]]></FromUserName>
      <CreateTime>12345678</CreateTime>
      <MsgType><![CDATA[text]]></MsgType>
      <Content><![CDATA[你好]]></Content>
    </xml>
    :param list:
    :return:
    """
    root = ET.Element("xml")
    toUsername = ET.SubElement(root, "ToUserName")
    fromUserName = ET.SubElement(root, "FromUserName")
    createTime = ET.SubElement(root, "CreateTime")
    msgType = ET.SubElement(root, "MsgType")
    content = ET.SubElement(root, "Content")
    toUsername.text = "<![CDATA[" + "oIPLH1P31seTfvqU2Gvr852DHS_Q" + "]]>"
    fromUserName.text = "<![CDATA[" + "gh_9715d2592755" + "]]>"
    createTime.text = 1234567890
    msgType.text = "<![CDATA[" + "text" + "]]>"
    content.text = "<![CDATA[" + "123123" + "]]>"
    result = ET.Element(root)
    print(str(result))
    return result


def createMenu():
    p = json.dumps(MENU, ensure_ascii=False)
    postUrl = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % AccessToken.get_access_token()
    rep = requests.post(postUrl, p.encode('utf-8'))
    if json.loads(rep.text).get("errmsg") == "ok":
        return True
    else:
        return False


def sendTemplateMsg(toUser="oIPLH1P31seTfvqU2Gvr852DHS_Q"):
    msg = {
        "touser": toUser,
        "template_id": "GqFgli7w9_T-h2NKjVX18l5cZGnRiZ_RzMnCWe7lzs8",
        "url": URL + "/main",
        "data": {
            "first": {
                "value":"推荐文章:",
                "color":"#173177"
            },
            "title": {
                "value":"【新闻聚焦】BTV新闻：积极推广防癌健康查体",
                "color":"#173177"
            }
        }
    }
    p = json.dumps(msg, ensure_ascii=False)
    # https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=ACCESS_TOKEN
    postUrl = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % AccessToken.get_access_token()
    rep = requests.post(postUrl, p.encode('utf-8'))
    if json.loads(rep.text).get("errmsg") == "ok":
        return True
    else:
        return False


def getUserList():
    url = "https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=%s" % (
        AccessToken.get_access_token(), NULL)
    rep = requests.get(url)
    return json.loads(rep.text).get("data")["openid"]


def uploadForeverMaterial():
    url = "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=%s&type=image" % (
        AccessToken.get_access_token())


def getOpenid():
    url = "https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=OPENID" %AccessToken.get_access_token()
    rep = requests.get(url)
    return json.loads(rep.text).get("openid")


def sendAll():
    data = {
   "filter":{
      "is_to_all":True,
   },
   "text":{
      "content":"CONTENT1"
   },
    "msgtype":"text",

}
    p = json.dumps(data,ensure_ascii=False)
    url = "https://api.weixin.qq.com/cgi-bin/message/mass/sendall?access_token=%s" %AccessToken.get_access_token()
    rep = requests.post(url,p.encode("utf-8"))
    if(json.loads(rep.text).get("errcode")==0):
        return True
    else:
        return False


def createMsg(_from,_to,_msg):
    xml = "<xml>" \
          "<ToUserName><![CDATA["\
          +_to+\
          "]]></ToUserName>" \
          "<FromUserName><![CDATA["+\
          _from\
          +"]]></FromUserName>" \
          "<CreateTime>12345678</CreateTime>" \
          "<MsgType><![CDATA[text]]></MsgType>" \
          "<Content><![CDATA["+\
          _msg\
          +"]]></Content>" \
          "</xml>"
    return xml


def sendByTag(tagid,msg):
    data = {
        "filter": {
            "is_to_all": False,
            "tag_id":tagid
        },
        "text": {
            "content": msg
        },
        "msgtype": "text",

    }
    p = json.dumps(data,ensure_ascii=False)
    url = "https://api.weixin.qq.com/cgi-bin/message/mass/sendall?access_token=%s" % AccessToken.get_access_token()
    rep = requests.post(url,p.encode('utf-8'))
    print(rep.text)


def createTag(tag):
    """
    创建标签
    接收：允许接收推送消息的用户组
    :return:rep
    {   "tag":{ "id":134,//标签id "name":"广东"   } }
    """
    data = {
        "tag":{
            "name":tag
        }
    }
    p = json.dumps(data, ensure_ascii=False)
    url = "https://api.weixin.qq.com/cgi-bin/tags/create?access_token=%s" %AccessToken.get_access_token()
    rep = requests.post(url,p.encode('utf-8'))
    return json.loads(rep.text).get("tag")


def removeTag(tagid):
    data = {   "tag":{        "id" : tagid   } }
    p = json.dumps(data, ensure_ascii=False)
    url = "https://api.weixin.qq.com/cgi-bin/tags/delete?access_token=%s" %AccessToken.get_access_token()
    rep = requests.post(url,p.encode('utf-8'))
    return json.loads(rep.text).get("errcode")==0


def getUserTags():
    """
    获取已有的全部标签及每个标签下用户数
    :return:tags 数组类型 元素如下：
    {
    "id":1,
    "name":"每天一罐可乐星人",
    "count":0 //此标签下粉丝数
    }
    """
    url = "https://api.weixin.qq.com/cgi-bin/tags/get?access_token=%s" %AccessToken.get_access_token()
    rep = requests.get(url)
    tags = json.loads(rep.text).get("tags")
    return tags


def setUserTag(list,tag):
    """
    批量为用户打标签
    post 数据示例
    {
        "openid_list" : [//粉丝列表
        "ocYxcuAEy30bX0NXmGn4ypqx3tI0",
        "ocYxcuBt0mRugKZ7tGAHPnUaOW7Y"   ],
        "tagid" : 134
     }
    :return:boolean
    """
    data = {
        "openid_list":list,
        "tagid":tag
    }
    p = json.dumps(data, ensure_ascii=False)
    url = "https://api.weixin.qq.com/cgi-bin/tags/members/batchtagging?access_token=%s" %AccessToken.get_access_token()
    rep = requests.post(url,p.encode('utf-8'))
    return json.loads(rep.text).get("errcode")==0


def removeUserTag(list,tagid):
    """
    批量为用户取消标签
    post 数据示例
    {
    "openid_list" : [//粉丝列表
    "ocYxcuAEy30bX0NXmGn4ypqx3tI0",
    "ocYxcuBt0mRugKZ7tGAHPnUaOW7Y"   ],
    "tagid" : 134
    }
    :return:boolean
    """
    data = {
        "openid_list":list,
        "tagid":tagid
    }
    p = json.dumps(data, ensure_ascii=False)
    url = "https://api.weixin.qq.com/cgi-bin/tags/members/batchuntagging?access_token=%s" %AccessToken.get_access_token()
    rep = requests.post(url,p.encode('utf-8'))
    return json.loads(rep.text).get("errcode")==0


def getUserListByTagID(tagid):
    data = {   "tagid" : tagid,   "next_openid":"" }
    url = "https://api.weixin.qq.com/cgi-bin/user/tag/get?access_token=%s" %AccessToken.get_access_token()
    p = json.dumps(data, ensure_ascii=False)
    rep = requests.post(url, p.encode('utf-8'))
    l = json.loads(rep.text).get("data")
    if l==None:
        return []
    else:
        return l["openid"]


if __name__ == '__main__':
    pass
    # print(createTag("订阅"))
    print(getUserTags())
    print(getUserListByTagID(102))
    # print(removeTag(101))
    # print(getUserTags())
