#项目启动入口
from flask_script import Manager
from app import create_app
from common.util import sendAll,createMenu
from myThread.myTimer import myTimer

#使用自定义计时器实现每天定时更新本地数据
# myTimer(0,0,"user","articles").start()
apps = create_app()
manage = Manager(app=apps)
createMenu()
sendAll()
from config import db
# myTimer(10,0).start()

if __name__ == '__main__':
    #manage.run(host='0.0.0.0')
    #db.create_all()
    manage.run()