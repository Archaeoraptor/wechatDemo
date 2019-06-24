from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


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