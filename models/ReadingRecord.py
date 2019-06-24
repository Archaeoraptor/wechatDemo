from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class UserReadingRecord(db.Model):
    __tablename__ = 'user_reading_record'
    idc_num = db.Column(db.CHAR(18),primary_key=True)
    record = db.Column(db.Text)
    def update_record(self,idc_num,article_id,reading_record):
        result = UserReadingRecord.query.filter_by(idc_num=idc_num).first()
        record = dict(eval(result.record))
        if(article_id not in record.keys()):
            record[article_id] = reading_record