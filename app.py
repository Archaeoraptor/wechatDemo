import json
import threading

import requests
from flask import request, Response, render_template, jsonify

from common.util import validate_wx_public,parseXML,createXML,createMenu,sendTemplateMsg,getUserList,sendAll,setUserTag,removeUserTag,getUserTags,createTag,getUserListByTagID,createMsg
from validate.form import WxpublicForm
from settings import APPID,APPSECRET,WECHATID
from flask_cors import *
from models.User import User
from models.Articles import Article
from models.MedicalRecord import MedicalRecord
from models.WechatToken import AccessToken
from models.ReadingRecord import UserReadingRecord
from config import app



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
# for user in getUserList():
#     sendTemplateMsg(user)
# # sendRecommendMsg()
# sendAll()


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
            xml = createMsg(WECHATID,userID,"点击查看最新推荐内容\nhttp://www.baidu.com")
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
    password = request.json.get("password")
    idc_num = request.json.get("idc_num")
    # name =
    result = User.query.filter_by(username=username).first()
    if username is None or password is None:
        return jsonify({
            'flag': 0,
            'errorText':'注册信息不合要求'
        })
    if result is not None:
        return jsonify({
            'flag': 2,
            'errorText':'用户名已存在'
        })
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.idc_num = idc_num
    db.session.commit()
    return jsonify({
        'flag':1
    })


@app.route('/login',methods=["GET","POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    result = User.query.filter_by(username=username).first()
    if result is None:
        return jsonify({
            "flag":2,
            "errorText":"用户名不存在"
        })
    if result is None or not result.check_password(password):
        return jsonify({
            'flag':0,
            'errorText':'用户名或密码错误'
        })
    if result.check_password(password):
        return jsonify({
            'flag': 1
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
    app.run(port=5003)
