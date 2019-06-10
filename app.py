import json
import threading

import requests
from flask import Flask, request, Response, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from common.util import validate_wx_public,parseXML,createXML,createMenu,sendTemplateMsg,getUserList,sendAll,setUserTag,removeUserTag,getUserTags,createTag,getUserListByTagID,createMsg

from werkzeug.security import generate_password_hash, check_password_hash
from validate.form import WxpublicForm
from settings import APPID,APPSECRET,WECHATID
from flask_cors import *

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Asdfghjkl123@211.83.111.224:3306/xw_utf8mb4'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

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


class User(db.Model):
    __tablename__ = 'recommender_user_info'
    idc_num = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(30),unique=True)
    password_hash = db.Column(db.String(255))
    def __repr__(self):
        return '<Role %r>' % self.username

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)


class Medical_record(db.Model):
    __tablename__ = 'medical_record'
    idc_num = db.Column(db.Integer,primary_key=True)


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    article = db.Column(db.Text)
    author = db.Column(db.String(255))
    c_date = db.Column(db.String(255))
    comment_id = db.Column(db.String(255))
    comment_num = db.Column(db.String(255))
    content_url = db.Column(db.String(255))
    like_num = db.Column(db.String(255))
    nickname = db.Column(db.String(255))
    p_date = db.Column(db.String(255))
    read_num = db.Column(db.String(255))
    reward_num = db.Column(db.String(255))
    title = db.Column(db.String(255))


class UserReadingRecord(db.Model):
    __tablename__ = 'user_reading_record'
    idc_num = db.Column(db.Integer,primary_key=True)
    record = db.Column(db.Text)
    def update_record(self,idc_num,article_id,reading_record):
        result = UserReadingRecord.query.filter_by(idc_num=idc_num).first()
        record = dict(eval(result.record))
        if(article_id not in record.keys()):
            record[article_id] = reading_record


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
