from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class MedicalRecord(db.Model):
    __tablename__ = 'user_medical_record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mr_id = db.Column(db.VARCHAR(11))
    profession = db.Column(db.Integer)
    idc_num = db.Column(db.char(18))
    realname = db.Column(db.VARCHAR(10))
    MZZD = db.Column((db.VARCHAR(20)))
    RYZD = db.Column((db.VARCHAR(20)))
    ZYZD = db.Column((db.VARCHAR(20)))
    QTZD = db.Column((db.VARCHAR(100)))
    BLZD = db.Column((db.VARCHAR(20)))
    icd_code = db.Column((db.VARCHAR(20)))
    age = db.Column(db.Integer)
    gender = db.Column(db.Integer)
    has_operation = db.Column(db.Integer)
    symptoms = db.Column(db.Text)
