#定时向用户发送网站推送，并初始化app
from views.user import user
from views.wechat import wechat
from views.recommender import recommender
from config import app
import flask_admin


def create_app():

    #注册蓝图
    app.register_blueprint(user,url_prefix="/")
    app.register_blueprint(wechat,url_prefix="/")
    app.register_blueprint(recommender,url_prefix="/")
    #admin = flask_admin.Admin(app, name='推送文章后台管理系统', template_mode='bootstrap4')
    #admin.add_view(sqla.ModelView(User, db.session))

    return app

def sendMsgRegularly():
    pass