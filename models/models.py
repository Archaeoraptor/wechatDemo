from urllib import request as re
import time
import requests
from flask import json
from settings import APPID,APPSECRET


class AccessToken(object):
    """
    获取token，用于修改菜单时校验token
    """
    access_token = {
        "access_token": "",
        "update_time": time.time(),
        "expires_in": 7200  #有效时间
    }

    @classmethod
    def get_access_token(cls):
        if not cls.access_token.get('access_token') or (
                time.time() - cls.access_token.get('update_time') > cls.access_token.get('expires_in')):
            url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
            APPID, APPSECRET)
            response = re.urlopen(url).read()
            resp_json = json.loads(response)
            if 'errcode' in resp_json:
                raise Exception(resp_json.get('errmsg'))
            else:
                cls.access_token['access_token'] = resp_json.get('access_token')
                cls.access_token['expires_in'] = resp_json.get('expires_in')
                cls.access_token['update_time'] = time.time()
                return cls.access_token.get('access_token')
        else:
            return cls.access_token.get('access_token')


