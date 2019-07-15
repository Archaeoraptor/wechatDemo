#项目启动入口
from flask_script import Manager
from app import create_app
from common.util import sendByTag
from myThread.myTimer import myTimer

#使用自定义计时器实现每天定时更新本地数据
# myTimer(0,0"user","articles").start()
app = create_app()
manage = Manager(app=app)
# myTimer(10,0).start()

if __name__ == '__main__':
    manage.run()