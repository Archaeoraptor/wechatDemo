from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

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