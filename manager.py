# 项目启动入口
from flask_script import Manager
from app import create_app
from common.util import sendAll, createMsg, createMenu
from flask_apscheduler import APScheduler
from myThread.myTimer import myTimer





# class Config(object):
#     JOBS = [
#         {
#             'id': 'send_daily',
#             'func': 'send_daily',
#             'args': '',
#             'trigger': {
#                 'type': 'cron',
#                 'day_of_week': "mon-fri",
#                 # 'hour': '6',
#                 # 'minute': '50',
#                 'second': '30'
#             }
#         }
#     ]
#
#
# scheduler = APScheduler()
# scheduler.init_app(app)
# scheduler.start()
# 使用自定义计时器实现每天定时更新本地数据
# myTimer(0,0,"user","articles").start()
# sendAll()
# flag_send = 1


apps = create_app()
manage = Manager(app=apps)
createMenu()
# if flag_send == 1:
#     sendAll()
#     flag_send = 0
#
sendAll()
from config import db

# myTimer(10,0).start()

if __name__ == '__main__':
    # manage.run(host='0.0.0.0')
    # db.create_all()
    manage.run()

