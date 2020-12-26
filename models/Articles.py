from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    resource = db.Column(db.VARCHAR(20))
    url = db.Column(db.VARCHAR(255))
    title = db.Column(db.VARCHAR(20))
    disease = db.Column(db.VARCHAR(10))
    label = db.Column(db.VARCHAR(20))
    content = db.Column(db.Text)