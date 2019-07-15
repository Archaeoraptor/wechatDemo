import threading
import time
from common.exportFromDB import getLastId,exportToCSV


class dataUpdate(threading.Thread):
    def __init__(self,tableName):
        threading.Thread.__init__(self)
        self.tableName = tableName

    def run(self):
        index = getLastId(self.tableName)
        exportToCSV(self.tableName,self.tableName,index)


if __name__ == '__main__':
    thread1 = dataUpdate("user")
    thread1.start()