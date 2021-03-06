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


user = Blueprint('users', __name__)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app=app)
admin = flask_admin.Admin(app, name='推送文章后台管理系统', template_mode='bootstrap4')
admin.add_view(sqla.ModelView(User, db.session))
admin.add_view(sqla.ModelView(RecommendArticle, db.session))
#admin = flask_admin.Admin(app, name='推送文章后台管理系统', template_mode='bootstrap4')
#admin.add_view(sqla.ModelView(User, db.session))

sendAll()

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
    data = {
        "latest": [
            {
            "url":"https://www.cn-healthcare.com/articlewm/20201227/content-1175558.html",
            "title":"关于肺小结节的实用科普",
            "from":"专家十问十答",
            "article_id":1,
            },
            {
            "url":"http://www.gzsums.net/news_25683.aspx",
            "title":"肝、肾离开人体依然可活多天 人离体活器官支持系统亮相广州",
            "from":"南方都市报",
            "article_id":2,
            },
            {
            "url":"https://m.sohu.com/a/440927209_120967",
            "title":"健康大咖谈|打赢健康保“胃”战",
            "from":"搜狐",
            "article_id":3,
            },
            {
            "url":"http://kpzg.people.com.cn/n1/2020/1010/c404214-31886402.html",
            "title":"塑料瓶装水经过暴晒会致癌？",
            "from":"人民网",
            "article_id":4,
            },
            {
            "url":"http://lxjk.people.cn/n1/2020/1218/c404177-31970835.html",
            "title":"15岁男孩患结肠癌",
            "from":"5个信号要警惕",
            "article_id":5,
            },
            {
            "url":"http://www.kepuchina.cn/more/202012/t20201224_2912255.shtml",
            "title":"首张不同癌症人体转移图问世",
            "from":"科普 中国",
            "article_id":1,
            },
            {
            "url":"https://3g.163.com/dy/article/FUJV8Q0505118405.html?spss=adap_pc",
            "title":"哪些人更容易得癌症？肿瘤医生：这五类人",
            "from":"网易新闻",
            "article_id":2,
            },
            {
            "url":"http://hi.people.com.cn/n2/2020/1224/c231190-34493303.html",
            "title":"中国癌症基金会“肺越未来”肺癌患者关爱项目落地海南",
            "from":"人民网",
            "article_id":3,
            },
            {
            "url":"https://m.sohu.com/a/439622957_359980/?pvid=000115_3w_a",
            "title":"华西科普 | 癌症会遗传、有传染性？专家：不是一份基因检测报告就能判断",
            "from":"搜狐健康",
            "article_id":4,
            },

            {
                "url": "http://health.people.com.cn/n1/2020/1222/c14739-31974499.html",
                "title": "坏情绪助推肿瘤发展 5种饮品改善情绪",
                "from": "来源：人民网",
                "article_id": 1
            },
            {
                "url": "http://health.people.cn/n1/2020/1223/c14739-31976041.html",
                "title": "高发的子宫肌瘤该拿它怎么办",
                "from": "来源：人民网",
                "article_id": 1
            },
            {
                "url": "https://www.medsci.cn/article/show_article.do?id=a1c120458837",
                "title": "世卫大会首次承诺要消除宫颈癌！女孩子都应该看的HPV疫苗科普干货",
                "from": "来源：MedSci梅斯医生",
                "article_id": 1
            },
            {
                "url": "https://3g.163.com/local/article/FUCNN2BU04398SNN.html?from=dynamic",
                "title": "16位肉瘤专家亲情奉献 中国首部软组织肉瘤领域科普书正式发布",
                "from": "来源：网易新闻",
                "article_id": 2
            },
            {
                "url": "http://www.cdctj.com.cn/system/2020/12/22/030041461.shtml",
                "title": "癌症知否：数学公式区分癌症和肿瘤",
                "from": "来源：CCFDIE平台",
                "article_id": 1
            },
            {
                "url": "http://www.caca.org.cn/system/2020/11/24/020046703.shtml",
                "title": "【防癌早知道】肺癌关注月：化疗在肺癌治疗中有何作用？",
                "from": "中国抗癌协会",
                "article_id": 50,
            },
            {
                "url": "https://www.kepuchina.cn/more/202012/t20201222_2907038.shtml",
                "title": "只在癌细胞内溶解的载药纳米颗粒",
                "from": "科普中国",
                "article_id": 50,
            },
            {
                "url": "https://m.thepaper.cn/newsDetail_forward_10495309",
                "title": "科普丨癌症来之前，都会经历“癌前病变”",
                "from": "澎湃新闻",
                "article_id": 50,
            },
            {
                "url": "http://www.xinhuanet.com/science/2019-04/19/c_137990321.htm",
                "title": "谈到肿瘤就害怕？这些说法不可信",
                "from": "新华网",
                "article_id": 50,
            },

        ],
        "recommend": recommend["recommend"]
    }
    # print("feiai:",recommend["recommend"])
    return render_template("index.html", data=data)


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