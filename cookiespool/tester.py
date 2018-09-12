#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from cookiespool.db import RedisClient
import json
import requests
from requests import ConnectionError
from cookiespool.config import *

#测试模块的父类
class ValidTester(object):
    #初始化一些对象
    def __init__(self,website='default'):
        self.website=website
        self.cookies_db=RedisClient('cookies',self.website)
        self.accounts_db=RedisClient('accounts',self.website)


    #测试cookies,子类需要重写
    def test(self,username,cookies):
        raise NotImplementedError


    #运行,得到所有cookies,依次测试
    def run(self):
        cookies_groups=self.cookies_db.all()
        for username,cookies in cookies_groups.items():
            self.test(username,cookies)



#对接测试微博cookies的子类,如需扩展其他站点,可再增加子类
class WeiboValidTester(ValidTester):
    #初始化操作
    def __init__(self,website='weibo'):
        ValidTester.__init__(self,website)

    #不同的站点有不同的测试方法
    def test(self,username,cookies):
        print('正在测试Cookies','用户名',username)
        try:
            cookies=json.loads(cookies)
        except TypeError:
            print('Cookies不合法',username)
            self.cookies_db.delete(username)
            print('Cookies删除',username)
            return
        try:
            test_url=TEST_URL_MAP[self.website]
            response=requests.get(test_url,cookies=cookies,timeout=5,allow_redirects=False)
            if response.status_code==200:
                print('Cookies有效',username)
            else:
                print(response.status_code, response.headers)
                print('Cookies失效',username)
                self.cookies_db.delete(username)
                print('删除Cookies',username)
        except ConnectionError as e:
            print('发生异常',e.args)

class XueqiuValidTester(ValidTester):
    def __init__(self,website='xueqiu'):
        ValidTester.__init__(self,website)


    def test(self,username,cookies):
        print('正在测试Cookies','用户名',username)
        try:
            cookies=json.loads(cookies)
        except TypeError:
            print('Cookies不合法',username)
            self.cookies_db.delete(username)
            print('Cookies删除',username)
            return
        try:
            test_url=TEST_URL_MAP[self.website]
            response=requests.get(test_url,cookies=cookies,timeout=5,allow_redirects=False)
            if response.status_code==200:
                print('Cookies有效',username)
            else:
                print(response.status_code, response.headers)
                print('Cookies失效',username)
                self.cookies_db.delete(username)
                print('删除Cookies',username)
        except ConnectionError as e:
            print('发生异常',e.args)


if __name__=='__main__':
    WeiboValidTester().run()






