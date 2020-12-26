#项目配置文件，包含数据库地址等
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from common.util import sendAll
app = Flask(__name__)
CORS(app, supports_credentials=True)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:xi102@dhcasdfghjkl@211.83.111.224:3308/xw_utf8mb4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@211.83.111.221:3308/xw_utf8mb4'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = "abc"
#app.config['']
db = SQLAlchemy(app)
db.create_all()

# @app.before_first_request
# def send_daily():
#     print("一次推送测试")
#     sendAll()
#     print("send_daily 执行了一次")