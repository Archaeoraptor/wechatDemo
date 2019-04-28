import json
import threading

import requests
from flask import Flask, request, Response, render_template
from common.util import validate_wx_public,parseXML,createXML,createMenu,sendTemplateMsg,getUserList
from validate.form import WxpublicForm
from settings import APPID,APPSECRET
app = Flask(__name__)
#创建menu自定义菜单
createMenu()
#获取关注用户列表，向全部用户发送推送
for user in getUserList():
    sendTemplateMsg(user)

@app.route('/',methods=['GET','POST'])
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
        parseXML(str)
        xml = "<xml>" \
              "<ToUserName><![CDATA[oIPLH1P31seTfvqU2Gvr852DHS_Q]]></ToUserName>" \
              "<FromUserName><![CDATA[gh_9715d2592755]]></FromUserName>" \
              "<CreateTime>12345678</CreateTime>" \
              "<MsgType><![CDATA[text]]></MsgType>" \
              "<Content><![CDATA[我是胖胡]]></Content>" \
              "</xml>"
        return Response(xml, mimetype='text/xml')


@app.route('/list/',methods=["GET","POST"])
def getList():
    return render_template("html/redirect.html")


@app.route('/list2/',methods=["GET","POST"])
def getList2():
    code = request.url.split("?code=")[1].split("&state")[0]
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code'%(APPID,APPSECRET,code)
    rep = requests.get(url)
    return render_template("html/list.html",msg = json.loads(rep.text).get("openid"))


if __name__ == '__main__':
    app.run()
