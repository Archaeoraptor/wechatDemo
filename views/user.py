from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models.User import User

db = SQLAlchemy()
user = Blueprint('user', __name__)


@user.route('/login', methods=["GET", "POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    result = User.query.filter_by(username=username).first()
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
        return jsonify({
            'flag': 1
        })


@user.route('/forget', methods=["GET", "POST"])
def forget():
    if (request.method == "GET"):
        return render_template("forget.html")
    if (request.method == "POST"):
        return jsonify({
            "flag": 1
        })


@user.route('/register', methods=["GET", "POST"])
def register():
    username = request.json.get("username")
    password = request.json.get("password")
    idc_num = request.json.get("idc_num")
    # name =
    result = User.query.filter_by(username=username).first()
    if username is None or password is None:
        return jsonify({
            'flag': 0,
            'errorText': '注册信息不合要求'
        })
    if result is not None:
        return jsonify({
            'flag': 2,
            'errorText': '用户名已存在'
        })
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.idc_num = idc_num
    db.session.commit()
    return jsonify({
        'flag': 1
    })


@user.route('/main', methods=["GET", "POST"])
def main_page():
    # 登录注册页面 命名就不吐槽了
    return render_template("main.html")


@user.route('/index', methods=["GET", "POST"])
def index():
    # 主页，即内容导航页面
    msg = "asd"
    # data = {}   # 从数据库获取文章数据，字典元素格式如下：key：文章所属板块，value：字典格式，{"url":"","title":"","from":"","article_id":""}
    # 待完成：在data字典中存入最新的若干条数据,对应key：latest
    # 待完成：根据模型，得到向用户推荐的若干条数据，在data字典中存入，受模型大小的影响，这一过程可能会比较耗时，拟采取ajax请求的方式获取
    data = {
        "latest": [
            {
                "url": "http://mp.weixin.qq.com/s?__biz=MzA4NzE5OTYzNg==&mid=2650952886&idx=1&sn=1aa62fb7343b7ffe9957b8f10293804a&chksm=8bcbee4dbcbc675b764877be8fa9ea75167787eb9b12f2a767db335d549fa160393a22d69ebf&scene=27#wechat_redirect",
                "title": "【新闻聚焦】BTV新闻：积极推广防癌健康查体",
                "from": "来源：中国医学科学院肿瘤医院",
                "article_id": 1
            },
            {
                "url": "http://mp.weixin.qq.com/s?__biz=MzA4NzE5OTYzNg==&mid=2650952886&idx=1&sn=1aa62fb7343b7ffe9957b8f10293804a&chksm=8bcbee4dbcbc675b764877be8fa9ea75167787eb9b12f2a767db335d549fa160393a22d69ebf&scene=27#wechat_redirect",
                "title": "【新闻聚焦】BTV新闻：积极推广防癌健康查体",
                "from": "来源：中国医学科学院肿瘤医院",
                "article_id": 2
            }
        ],
        "recommend": [{
            "url": "http://mp.weixin.qq.com/s?__biz=MzA4NzE5OTYzNg==&mid=2650952886&idx=1&sn=1aa62fb7343b7ffe9957b8f10293804a&chksm=8bcbee4dbcbc675b764877be8fa9ea75167787eb9b12f2a767db335d549fa160393a22d69ebf&scene=27#wechat_redirect",
            "title": "【新闻聚焦】BTV新闻：积极推广防癌健康查体",
            "from": "中国医学科学院肿瘤医院",
            "article_id": 1
        }]
    }
    return render_template("index.html", data=data)

@user.route('/callback', methods=["POST"])
def callback():
    # 用户习惯反馈接口 接口内容：用户ID，偏好的文章ID，浏览时长，减少推荐的文章ID，用户操作编码code（2代表减少推荐，其他待定）
    code = request.json.get("code")
    print("code"+str(code))
    # 数据库操作,需要建用户浏览习惯数据表，字段待完善
    return jsonify({
        'flag': 1
    })