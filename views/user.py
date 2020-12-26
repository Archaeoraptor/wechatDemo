from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from common.util import isUsernameValid, isPasswordValid, isIDCumValid, isNameValid
from models.User import User
from config import db,app
from static_data import *
import random
from common.util import sendAll

from flask_login import LoginManager,login_user,login_required,current_user,logout_user
# from wtform import StringField,BooleanField,PasswordField
# from wtform.validators import DataRequired

#db = SQLAlchemy()

user = Blueprint('user', __name__)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app=app)

sendAll()

@login_manager.user_loader
def load_user(username):
    this_user = db.session.query(User).filter_by(username=username).first()
    return this_user




@user.route('/login', methods=["GET", "POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    #result = User.query.filter_by(username=username).first()
    result = db.session.query(User).filter_by(username=username).first()
    this_user = User(username=username)
    this_user.set_phone_num(password)
    this_user.set_password(password)
    #result = db.engine.execute('select * from user_info where username = "'+username+'"').first()
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
        #print(this_user)
        login_user(this_user)
        return jsonify({
            'flag': 1,
            'cancer_type': result.get_mr_id()
        })

@user.route('/submit_table', methods=["GET", "POST"])
#@login_required
def setType():
    cancer_type = request.json.get("type")
    #写入数据库
    print("当前登录下来的用户是",end=":")
    print(current_user.username)
    username = request.json.get('username')
    password = request.json.get('password')
    cancer_type = request.json.get('type')
    this_user = db.session.query(User).filter_by(username=username).first()
    print("然而我们查询到的是",end=":")
    print(this_user)
    if this_user.check_password(password):
        this_user.mr_id = cancer_type
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


#@user.route('/index', methods=["GET", "POST"])
@user.route('/table',methods=["GET","POST"])
def table():
    return render_template("table.html")

@user.route('/index/<type>', methods=["GET", "POST"])
def index(type):
    print(type)
    # data_feiai, data_ganai, data_pifuai, data_gongjingai, data_weichangdaozhongliu
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

    # 主页，即内容导航页面
    msg = "asd"
    # data = {}   # 从数据库获取文章数据，字典元素格式如下：key：文章所属板块，value：字典格式，{"url":"","title":"","from":"","article_id":""}
    # 待完成：在data字典中存入最新的若干条数据,对应key：latest
    # 待完成：根据模型，得到向用户推荐的若干条数据，在data字典中存入，受模型大小的影响，这一过程可能会比较耗时，拟采取ajax请求的方式获取
    data = {
        "latest": [
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
                "article_id": 2
            },
            {
                "url": "https://www.medsci.cn/article/show_article.do?id=a1c120458837",
                "title": "世卫大会首次承诺要消除宫颈癌！女孩子都应该看的HPV疫苗科普干货",
                "from": "来源：MedSci梅斯医生",
                "article_id": 3
            },
            {
                "url": "https://3g.163.com/local/article/FUCNN2BU04398SNN.html?from=dynamic",
                "title": "16位肉瘤专家亲情奉献 中国首部软组织肉瘤领域科普书正式发布",
                "from": "来源：网易新闻",
                "article_id": 4
            },
            {
                "url": "http://www.cdctj.com.cn/system/2020/12/22/030041461.shtml",
                "title": "癌症知否：数学公式区分癌症和肿瘤",
                "from": "来源：CCFDIE平台",
                "article_id": 5
            },
            {
                "url": "http://www.caca.org.cn/system/2020/11/24/020046703.shtml",
                "title": "【防癌早知道】肺癌关注月：化疗在肺癌治疗中有何作用？",
                "from": "中国抗癌协会",
                "article_id": 6,
            },
            {
                "url": "https://www.kepuchina.cn/more/202012/t20201222_2907038.shtml",
                "title": "只在癌细胞内溶解的载药纳米颗粒",
                "from": "科普中国",
                "article_id": 7,
            },
            {
                "url": "https://m.thepaper.cn/newsDetail_forward_10495309",
                "title": "科普丨癌症来之前，都会经历“癌前病变”",
                "from": "澎湃新闻",
                "article_id": 8,
            },
            {
                "url": "http://www.xinhuanet.com/science/2019-04/19/c_137990321.htm",
                "title": "谈到肿瘤就害怕？这些说法不可信",
                "from": "新华网",
                "article_id": 9,
            },

        ],
        "recommend": recommend["recommend"]
    }
    # print(random.shuffle(recommend["recommend"]))
    random.shuffle(recommend["recommend"])
    print(recommend["recommend"])
    return render_template("index.html", data=data)


@user.route('/callback', methods=["POST"])
def callback():
    # 用户习惯反馈接口 code=1表示浏览时长 暂时只有编码1，之后与用户主动评分等反馈，可以添加其他编码
    code = request.json.get("code")
    data = request.json.get("data")
    article_id = data["article_id"]
    read_time = data["read_time"]
    username = data["username"]
    print(data)
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


