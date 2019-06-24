from urllib import request as re
import time
import requests
from flask import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from settings import APPID,APPSECRET

db = SQLAlchemy()
class User(db.Model):
    __tablename__ = 'recommender_user_info'
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    idc_num = db.Column(db.CHAR(18),unique=True)
    realname = db.Column(db.VARCHAR(10))
    username = db.Column(db.VARCHAR(10),unique=True)
    password_hash = db.Column(db.VARCHAR(255))
    def __repr__(self):
        return '<Role %r>' % self.username

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)


class Medical_record(db.Model):
    __tablename__ = 'medical_record'
    idc_num = db.Column(db.CHAR(18),primary_key=True)


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    article = db.Column(db.Text)
    author = db.Column(db.VARCHAR())
    c_date = db.Column(db.VARCHAR(255))
    comment_id = db.Column(db.VARCHAR(255))
    comment_num = db.Column(db.VARCHAR(255))
    content_url = db.Column(db.VARCHAR(255))
    like_num = db.Column(db.VARCHAR(255))
    nickname = db.Column(db.VARCHAR(255))
    p_date = db.Column(db.VARCHAR(255))
    read_num = db.Column(db.VARCHAR(255))
    reward_num = db.Column(db.VARCHAR(255))
    title = db.Column(db.VARCHAR(255))


class UserReadingRecord(db.Model):
    __tablename__ = 'user_reading_record'
    idc_num = db.Column(db.CHAR(18),primary_key=True)
    record = db.Column(db.Text)
    def update_record(self,idc_num,article_id,reading_record):
        result = UserReadingRecord.query.filter_by(idc_num=idc_num).first()
        record = dict(eval(result.record))
        if(article_id not in record.keys()):
            record[article_id] = reading_record


class AccessToken(object):
    """
    获取token，用于修改菜单时校验token
    """
    access_token = {
        "access_token": "",
        "update_time": time.time(),
        "expires_in": 7200  #有效时间
    }

    @classmethod
    def get_access_token(cls):
        if not cls.access_token.get('access_token') or (
                time.time() - cls.access_token.get('update_time') > cls.access_token.get('expires_in')):
            url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
            APPID, APPSECRET)
            response = re.urlopen(url).read()
            resp_json = json.loads(response)
            if 'errcode' in resp_json:
                raise Exception(resp_json.get('errmsg'))
            else:
                cls.access_token['access_token'] = resp_json.get('access_token')
                cls.access_token['expires_in'] = resp_json.get('expires_in')
                cls.access_token['update_time'] = time.time()
                return cls.access_token.get('access_token')
        else:
            return cls.access_token.get('access_token')


