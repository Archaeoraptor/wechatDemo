#定时向用户发送网站推送，并初始化app
from views.user import user
from views.wechat import wechat
from config import app
from views.recommender import recommender


def create_app():

    #注册蓝图
    app.register_blueprint(user,url_prefix="/")
    app.register_blueprint(wechat,url_prefix="/")
    app.register_blueprint(recommender,url_prefix="/")
    return app

def sendMsgRegularly():
    pass