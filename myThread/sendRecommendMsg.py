import threading

from common.util import sendByTag


class dataUpdate(threading.Thread):
    def __init__(self,tableName):
        threading.Thread.__init__(self)
        self.tableName = tableName

    def run(self):
        print("send recommend message")
        sendByTag(102, "点击查看最新的推荐内容\nhttps://uestctest.cn1.utools.club/main")
