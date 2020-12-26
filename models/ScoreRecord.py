from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class UserScoreRecord(db.Model):
    __tablename__ = 'user_reading_record'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer)
    article_id = db.Column(db.Integer)
    score = db.Column(db.Integer)