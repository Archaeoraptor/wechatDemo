import json
import threading

import requests
from flask import Flask, request, Response, render_template, jsonify, redirect, url_for
from common.util import validate_wx_public,parseXML,createXML,createMenu,sendTemplateMsg,getUserList,getOpenid
from validate.form import WxpublicForm
from settings import APPID,APPSECRET
from flask_cors import *


app = Flask(__name__)
CORS(app, supports_credentials=True)
#创建menu自定义菜单
createMenu()
#获取关注用户列表，向全部用户发送推送
# def sendRecommendMsg():
#     for user in getUserList():
#         # delWithUsers() 根据用户，选择推荐消息内容
#         sendTemplateMsg(user)
#     global timer
#     timer = threading.Timer(3, sendRecommendMsg)
#     timer.start()
for user in getUserList():
    sendTemplateMsg(user)
# sendRecommendMsg()

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
    return render_template("redirect.html")


@app.route('/list2/',methods=["GET","POST"])
def getList2():
    code = request.url.split("?code=")[1].split("&state")[0]
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code'%(APPID,APPSECRET,code)
    rep = requests.get(url)
    openid = json.loads(rep.text).get("openid")
    # generateRecommentList() #根据用户openid生成推荐文章列表
    print(openid)
    return render_template("index.html", openid = openid)


@app.route('/index',methods=["GET","POST"])
def index():
    return render_template("index.html")


@app.route('/main',methods=["GET","POST"])
def main_page():
    return render_template("main.html")


@app.route('/register',methods=["GET","POST"])
def register():
    username = request.json.get("username")
    useremail = request.json.get("useremail")
    phone = request.json.get("phone")
    password = request.json.get("password")
    return jsonify({
        "flag":1
    })


@app.route('/login',methods=["GET","POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    print(username)
    print(password)
    return jsonify({
        "flag":1
    })


@app.route('/forget',methods=["GET","POST"])
def forget():
    if(request.method=="GET"):
        return render_template("forget.html")
    if(request.method=="POST"):
        return jsonify({
            "flag":1
        })

if __name__ == '__main__':
    app.run()
