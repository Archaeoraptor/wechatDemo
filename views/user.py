from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from common.util import isUsernameValid, isPasswordValid, isIDCumValid, isNameValid
from models.User import User,ReadLog,SurveyResult,RecommendArticle
from config import db,app,babel
from static_data import *
import random

from flask_login import LoginManager,login_user,login_required,current_user,logout_user
# from wtform import StringField,BooleanField,PasswordField
# from wtform.validators import DataRequired
from common.util import sendAll
#db.create_all()

import flask_admin
from flask_admin.base import MenuLink
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from flask_admin.contrib.sqla.filters import BaseSQLAFilter, FilterEqual
from flask_admin.babel import gettext
from models.User import User
from sqlalchemy import inspect


user = Blueprint('users', __name__)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app=app)
admin = flask_admin.Admin(app, name='推送文章后台管理系统', template_mode='bootstrap4')

class UserModelView(sqla.ModelView):
    column_labels = dict(username='用户名', password_hash='密码Hash',mr_id='疾病类别', phone_num='电话号码')


class ArticleModelView(sqla.ModelView):
    column_labels = dict(article_tag='标签', article_title='文章标题',article_source='文章来源', article_link='文章链接')

class RecordModelView(sqla.ModelView):
    column_labels = dict(read_link='文章链接', time='阅读时长（秒）',username='姓名', phone_num='电话号码')
    column_hide_backrefs = False
    column_list = [c_attr.key for c_attr in inspect(ReadLog).mapper.column_attrs]

admin.add_view(UserModelView(User, db.session, u'订阅用户'))
admin.add_view(ArticleModelView(RecommendArticle, db.session, u'推送文章'))
admin.add_view(RecordModelView(ReadLog, db.session, u'阅读记录'))
#admin = flask_admin.Admin(app, name='推送文章后台管理系统', template_mode='bootstrap4')
#admin.add_view(sqla.ModelView(User, db.session))

# sendAll()

@login_manager.user_loader
def load_user(phone):
    usr = db.session.query(User).filter_by(phone_num=phone).first()
    return usr

@user.route('/logout', methods=["POST"])
def logout():
    logout_user()
    return jsonify({
        "flag":1
    })

@user.route('/login', methods=["GET", "POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    #result = User.query.filter_by(username=username).first()有缓存问题
    result = db.session.query(User).filter_by(username=username).first()
    print("查到了这个",end=":")
    print(result)
    if result is None:
        return jsonify({
            "flag": 2,
            "errorText": "用户名不存在"
        })
    if result is None or not result.check_password(password):
        return jsonify({
            'flag': 0,
            'errorText': '用户名或密码错误'
        })
    if result.check_password(password):
        login_user(result)
        print("这个用户的mr_id是",end="[")
        print(result.get_mr_id(),end="")
        print("]")
        if result.get_mr_id() != '' and result.get_mr_id() is not None:
            return jsonify({
                'flag': 1,
                'cancer_type': cancer_type[result.get_mr_id()]
            })
        else:
            return jsonify({
                'flag': 1,
                'cancer_type': ''
            })

@user.route('/submit_table', methods=["GET", "POST"])
#@login_required
def setType():
    cancer_type_ = cancer_type_inverse[request.json.get("type")]
    year = request.json.get("year")
    treatment = request.json.get("treatment")
    institude = request.json.get("institude")
    retreatment = request.json.get("retreatment")
    channel = request.json.get("channel")
    interest = request.json.get("interest")
    method = request.json.get("method")
    frequency = request.json.get("frequency")
    #print("频率为", frequency)
    #写入数据库
    print("当前登录下来的用户是",end=":")
    print(current_user)
    if current_user is not None:
        current_user.mr_id = cancer_type_
        #print("现在写入库中的类型%s" % cancer_type_)
        '''
        survey_table = SurveyResult(
            Name=current_user.get_username(),
            Tel=current_user.get_phone(),
            CategoryCode='WJ001',
            Answer1=cancer_type_,
            Answer2=year,
            Answer3=institude,
            Answer4=treatment,
            Answer5=retreatment,
            Answer6=channel,
            Answer7=interest,
            Answer8=method,
            Answer9=frequency)
        '''
        survey_table = SurveyResult(
            current_user.get_username(),
            current_user.get_phone(),
            'WJ001',
            cancer_type_,
            year,
            institude,
            treatment,
            retreatment,
            channel,
            interest,
            method,
            frequency)
        # survey_table.Answer1 = cancer_type_
        # survey_table.Answer2 = year
        # survey_table.Answer3 = institude
        # survey_table.Answer4 = treatment
        # survey_table.Answer5 = retreatment
        # survey_table.Answer6 = channel
        # survey_table.Answer7 = interest
        # survey_table.Answer8 = method
        # survey_table.Answer9 = frequency
        db.session.add(survey_table)
        db.session.commit()
        return jsonify({
            "flag": 1
        })
    else:
        return jsonify({
            "flag":2
        })


@user.route('/forget', methods=["GET", "POST"])
def forget():
    if (request.method == "GET"):
        return render_template("forget.html")
    if (request.method == "POST"):
        return jsonify({
            "flag": 1
        })

#py -3 manager.py runserver --host 0.0.0.0 --port 5000
@user.route('/register', methods=["GET", "POST"])
def register():
    username = request.json.get("username")
    password = request.json.get("password")
    print("注册",end=':')
    print(username)
    #print(password)
    result = User.query.filter_by(username=username).first()
    if result is not None:
        #print(result)
        return jsonify({
            'flag': 2,
            'errorText': '用户名已存在'
        })
    # elif not (isUsernameValid(username) and isPasswordValid(password)):
    #     return jsonify({
    #         'flag': 0,
    #         'errorText': '注册信息不合要求'
    #     })
    user = User(username=username)
    user.set_password(password)
    user.set_phone_num(password)
    db.session.add(user)
    db.session.commit()
    #db.session.expire_all()
    return jsonify({
        'flag': 1
    })

@user.route('/main', methods=["GET", "POST"])
def main_page():
    # 登录注册页面 命名就不吐槽了
    return render_template("main.html")

@user.route('/table',methods=["GET","POST"])
def table():
    return render_template("table.html")

#@login_required
@user.route('/index/<type>', methods=["GET", "POST"])
def index(type):
    print(type)
    recommend = []
    if type == '肺癌':
        recommend = data_feiai
    elif type == '乳腺癌':
        recommend = data_ruxianai
    elif type == '肝癌':
        recommend = data_ganai
    elif type == '食管癌':
        recommend = data_shiguanai
    elif type == '结直肠癌':
        recommend = data_jiezhichangai
    elif type == '胃癌':
        recommend = data_weiai
    elif type == '甲状腺癌':
        recommend = data_jiazhuagnxianai
    elif type == '宫颈癌':
        recommend = data_gongjingai
    else:
        recommend = data_qita
    random.shuffle(recommend["recommend"])
    # 主页，即内容导航页面
    msg = "asd"
    # data = {}   # 从数据库获取文章数据，字典元素格式如下：key：文章所属板块，value：字典格式，{"url":"","title":"","from":"","article_id":""}
    # 待完成：在data字典中存入最新的若干条数据,对应key：latest
    # 待完成：根据模型，得到向用户推荐的若干条数据，在data字典中存入，受模型大小的影响，这一过程可能会比较耗时，拟采取ajax请求的方式获取
    data_db = db.session.query(RecommendArticle).filter_by(article_tag=type)
    data2 = {
        "latest":[],
        "recommend":[]
        }
    for line in data_db:
        data2["recommend"].append({
            "url": line.get_article_link(),
            "title": line.get_article_title(),
            "from": line.get_article_source(),
            "article_id": line.get_id(),
        })
    data_latest = db.session.query(RecommendArticle).filter_by(article_tag='最新')
    for line in data_latest:
        data2["latest"].append({
            "url": line.get_article_link(),
            "title": line.get_article_title(),
            "from": line.get_article_source(),
            "article_id": line.get_id(),
        })
    return render_template("index.html", data=data2)


@user.route('/callback', methods=["POST"])
def callback():
    # 用户习惯反馈接口 code=1表示浏览时长 暂时只有编码1，之后与用户主动评分等反馈，可以添加其他编码

    article_id = request.json.get("article_id")
    # TODO 上传用户的浏览时长，用户ID-文章ID-时长
    try:
        #上传的代码，用户表需要建立索引，或者修改为前端传递用户ID
        return jsonify({
            'flag': 1
        })
        pass
    except:
        return jsonify({
            'flag': 0,
            'errorText':""
        })

@user.route('/acknow',methods=["GET","POST"])
def acknow():
    return render_template("acknow.html")

@user.route('/add_reading_record', methods=["POST"])
def addReadingRecord():
    read_link = request.json.get("read_link")
    username = current_user.get_username()
    phone = current_user.get_phone()
    print("现在向数据库写入阅读记录数据:"+phone+"|"+username+"|"+read_link)
    read_log = ReadLog(username,phone,read_link)
    db.session.add(read_log)
    db.session.commit()
    return jsonify({
        'flag':1
    })

@user.route('/admin',methods=["GET","POST"])
def myAdmin():
    return render_template("admin.html")