import requests
import json

from settings import TOKEN, MENU, TEMPLATE_MSG, NULL, URL
import xml.etree.ElementTree as ET
import hashlib
from models import AccessToken


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
    # for el in root:
    #     print(el.tag)
    #     print(el.text)


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
    content.text = "<![CDATA[" + "滚。。" + "]]>"
    result = ET.Element(root)
    print(str(result))
    return result


def createMenu():
    p = json.dumps(MENU, ensure_ascii=False)
    print("--->" + AccessToken.get_access_token())
    postUrl = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % AccessToken.get_access_token()
    req = requests.post(postUrl, p.encode('utf-8'))
    print(req.text)


def sendTemplateMsg(toUser="oIPLH1P31seTfvqU2Gvr852DHS_Q"):
    msg = {
        "touser": toUser,
        "template_id": "GqFgli7w9_T-h2NKjVX18l5cZGnRiZ_RzMnCWe7lzs8",
        "url": URL + "/list/",
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
    print("--->" + AccessToken.get_access_token())
    # https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=ACCESS_TOKEN
    postUrl = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % AccessToken.get_access_token()
    req = requests.post(postUrl, p.encode('utf-8'))
    print(req.text)


def getUserList():
    url = "https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=%s" % (
        AccessToken.get_access_token(), NULL)
    rep = requests.get(url)
    return json.loads(rep.text).get("data")["openid"]


def uploadForeverMaterial():
    url = "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=%s&type=image" % (
        AccessToken.get_access_token())


if __name__ == '__main__':
    print(AccessToken.get_access_token())
