#项目启动入口
from flask_script import Manager
from app import create_app
from common.util import sendByTag

app = create_app()
manage = Manager(app=app)
sendByTag(102, "12")
if __name__ == '__main__':
    manage.run()