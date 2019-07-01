import json
import requests
from settings import APPID,APPSECRET,WECHATID
from flask import Blueprint, request, render_template, Response
from common.util import validate_wx_public, parseXML, getUserTags, getUserListByTagID, createMsg, setUserTag, createTag, \
    removeUserTag

from validate.form import WxpublicForm

wechat = Blueprint('wechat', __name__)


@wechat.route('/',methods=['GET','POST'])
def validate():
    if request.method == 'GET':
        data = request.args.to_dict()
        form = WxpublicForm(**data)
        if form.validate():
            result = validate_wx_public(form)
            if result[0]:
                return result[1]
        else:
            ValueError
    else:
        str = request.get_data()
        result = parseXML(str)
        userID = result[0]
        if len(result) == 2 and result[1] == "订阅":
            l = getUserTags()
            flag = False
            for dic in l:
                if (dic["name"] == "订阅"):
                    tagID = dic["id"]
                    flag = True
                    break
            if flag:
                if userID in getUserListByTagID(tagID):
                    xml = createMsg(WECHATID, userID, "已订阅，无须重复订阅！")
                    return Response(xml, mimetype='text/xml')
                else:
                    setUserTag([userID],tagID)
                    xml = createMsg(WECHATID,userID,"订阅成功！")
                    return Response(xml, mimetype='text/xml')
            else:
                tagID = createTag("订阅")
                setUserTag([userID], tagID)
                xml = createMsg(WECHATID,userID,"订阅成功！")
                return Response(xml, mimetype='text/xml')
        elif len(result) == 2 and result[1] == "取消订阅":
            l = getUserTags()
            flag = False
            tagID = -1
            for dic in l:
                if (dic["name"] == "订阅"):
                    tagID = dic["id"]
                    flag = True
                    break
            if flag:
                if userID in getUserListByTagID(tagID):
                    removeUserTag([userID],tagID)
                    xml = createMsg(WECHATID,userID,"取消订阅成功！")
                    return Response(xml, mimetype='text/xml')
        else:
            # xml = createMsg(WECHATID,userID,"回复\"订阅\"开启消息推送，回复\"取消订阅\"关闭消息推送")
            xml = createMsg(WECHATID,userID,"点击查看最新推荐内容\nhttp://xing.easy.echosite.cn/main")
            return Response(xml, mimetype='text/xml')


@wechat.route('/list/',methods=["GET","POST"])
def getList():
    return render_template("redirect.html")


@wechat.route('/list2/',methods=["GET","POST"])
def getList2():
    code = request.url.split("?code=")[1].split("&state")[0]
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code'%(APPID,APPSECRET,code)
    rep = requests.get(url)
    openid = json.loads(rep.text).get("openid")
    # generateRecommentList() #根据用户openid生成推荐文章列表
    print(openid)
    return render_template("index.html", openid = openid)