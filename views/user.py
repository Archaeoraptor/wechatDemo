from flask import Blueprint, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from models.User import User
db = SQLAlchemy()
user = Blueprint('user',__name__)


@user.route('/login',methods=["GET","POST"])
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


@user.route('/forget',methods=["GET","POST"])
def forget():
    if(request.method=="GET"):
        return render_template("forget.html")
    if(request.method=="POST"):
        return jsonify({
            "flag":1
        })


@user.route('/register',methods=["GET","POST"])
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


@user.route('/main',methods=["GET","POST"])
def main_page():
    return render_template("main.html")


@user.route('/index',methods=["GET","POST"])
def index():
    return render_template("index.html")