# 自定义线程，用于更新本地数据，供模型训练
import threading
from common.exportFromDB import getLastId,exportToCSV


class dataUpdate(threading.Thread):
    def __init__(self,tableName):
        threading.Thread.__init__(self)
        self.tableName = tableName

    def run(self):
        print("importing")
        index = getLastId(self.tableName)
        exportToCSV(self.tableName,self.tableName,index)


if __name__ == '__main__':
    thread1 = dataUpdate("user")
    thread2 = dataUpdate("user2")
    thread1.start()
    thread2.start()
    print("finish")