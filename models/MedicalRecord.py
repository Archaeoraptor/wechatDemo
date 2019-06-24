from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class MedicalRecord(db.Model):
    __tablename__ = 'medical_record'
    idc_num = db.Column(db.CHAR(18),primary_key=True)