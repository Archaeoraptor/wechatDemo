from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

#db = SQLAlchemy()
from config import db


class User(db.Model,UserMixin):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.VARCHAR(10), unique=True,index=True)
    password_hash = db.Column(db.VARCHAR(255))
    mr_id = db.Column(db.VARCHAR(11))
    phone_num = db.Column(db.CHAR(11))

    def get_mr_id(self):
        return self.mr_id

    def __repr__(self):
        return '<Role %r>' % self.username

    def set_phone_num(self, phone):
        self.phone_num = phone

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class ReadLog(db.Model):
    __tablename__ = 'read_log'
    username = db.Column(db.VARCHAR(10), db.ForeignKey('user_info'))
    phone_num = db.Column(db.VARCHAR(11), db.ForeignKey('user_info.phone_num'), primary_key=True)
    read_link = db.Column(db.VARCHAR(255), nullable=True)
    time = db.Column(db.Integer, nullable=True, default=0)

    def setReadLink(self, link):
        self.read_link = link

    def __repr__(self):
        return '<ReadLog %r>' % self.username