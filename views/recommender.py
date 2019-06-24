from flask import Blueprint, request, jsonify, render_template

from models.User import User

recommender = Blueprint('recommender',__name__)


def init_blue(app):
  app.register_blueprint(blueprint=recommender)


@recommender.route('/login',methods=["GET","POST"])
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


@recommender.route('/forget',methods=["GET","POST"])
def forget():
    if(request.method=="GET"):
        return render_template("forget.html")
    if(request.method=="POST"):
        return jsonify({
            "flag":1
        })