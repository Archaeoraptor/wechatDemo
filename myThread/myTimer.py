# 自定义计时器，定期循环执行本地数据更新以及模型训练
import datetime
import time
import threading
from myThread.dataUpdate import dataUpdate


class myTimer(threading.Thread):
    def __init__(self,hour=0,minute=0,*tableNames):
        threading.Thread.__init__(self)
        self.tableNames = [x for x in tableNames]
        self.hour = hour
        self.minute = minute

    def run(self):
        while True:
            # 判断是否达到设定时间，例如0:00
            while True:
                now = datetime.datetime.now()
                # 到达设定时间，结束内循环
                if now.hour == self.hour and now.minute == self.minute:
                    self.startTask()
                    break
            time.sleep()

    def startTask(self):
        for tableName in self.tableNames:
            dataUpdate(tableName).start()


if __name__ == '__main__':
    myTimer = myTimer(21,31,"user","user")
    myTimer.start()