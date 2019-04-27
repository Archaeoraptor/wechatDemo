from wtforms import Form, IntegerField, StringField
from wtforms.validators import DataRequired


class WxpublicForm(Form):
    timestamp = IntegerField(validators=[DataRequired(message="timestamp不能为空")])
    nonce = StringField(validators=[DataRequired(message="nonce不能为空")])
    signature = IntegerField(validators=[DataRequired(message="signature不能为空")])
    echostr = IntegerField(validators=[DataRequired(message="echostr不能为空")])
