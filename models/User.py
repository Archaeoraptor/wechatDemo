from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

#db = SQLAlchemy()
from config import db


class User(db.Model,UserMixin):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.VARCHAR(10), unique=True, index=True, nullable=False)
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

    def get_id(self):
        return self.phone_num

    def get_username(self):
        return self.username

    def get_phone(self):
        return self.phone_num

class ReadLog(db.Model):
    __tablename__ = 'read_log'
    log_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.VARCHAR(10), db.ForeignKey('user_info.username', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    phone_num = db.Column(db.VARCHAR(11))
    read_link = db.Column(db.VARCHAR(255), nullable=True)
    time = db.Column(db.Integer, nullable=True, default=0)

    def setReadLink(self, link):
        self.read_link = link

    def __repr__(self):
        return '<ReadLog %r | %r>' % (self.username, self.read_link)

    def __init__(self,name,phone,link):
        self.username = name
        self.phone_num = phone
        self.read_link = link

class SurveyResult(db.Model):
    __tablename__ = 'survey_result'
    ID = db.Column(db.INTEGER,autoincrement=True, primary_key=True)
    Name = db.Column(db.VARCHAR(255))
    Tel = db.Column(db.VARCHAR(255))
    CategoryCode = db.Column(db.VARCHAR(255))
    Answer1 = db.Column(db.VARCHAR(255))
    Answer2 = db.Column(db.VARCHAR(255))
    Answer3 = db.Column(db.VARCHAR(255))
    Answer4 = db.Column(db.VARCHAR(255))
    Answer5 = db.Column(db.VARCHAR(255))
    Answer6 = db.Column(db.VARCHAR(255))
    Answer7 = db.Column(db.VARCHAR(255))
    Answer8 = db.Column(db.VARCHAR(255))
    Answer9 = db.Column(db.VARCHAR(255))
    
    def __repr__(self):
        return '<SurveyResult %r>' % (self.Name)
    
    def __init__(self,name,tel,cat,a1,a2,a3,a4,a5,a6,a7,a8,a9):
        self.Name = name
        self.Tel = tel
        self.CategoryCode = cat
        self.Answer1 = a1
        self.Answer2 = a2
        self.Answer3 = a3
        self.Answer4 = a4
        self.Answer5 = a5
        self.Answer6 = a6
        self.Answer7 = a7
        self.Answer8 = a8
        self.Answer9 = a9


class RecommendArticle(db.Model):
    __tablename__ = 'recommend_article'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    article_title = db.Column(db.VARCHAR(255), unique=False, nullable=False)
    article_link = db.Column(db.VARCHAR(255), unique=False, nullable=False)
    article_source = db.Column(db.VARCHAR(255), unique=False, nullable=True)
    article_tag = db.Column(db.VARCHAR(20), unique=False)

    def __repr__(self):
        return '<Role %r>' % self.username

    def get_article_title(self):
        return self.article_title

    def get_article_link(self):
        return self.article_link

    def get_article_source(self):
        return self.article_source

    def get_article_tag(self):
        return self.article_tag

    def get_id(self):
        return self.id

db.create_all()