import threading
import json
from common.util import sendAll


def run():
    print("正在群发消息")
    sendAll()

def hello():
    print("已经发送了一条群发消息")

run()
hello()