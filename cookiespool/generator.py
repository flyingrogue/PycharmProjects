#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import json
from config import *
from db import RedisClient
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from weibocookies import WeiboCookies

#生成模块的父类
class CookiesGenerator(object):
    #初始化一些对象
    def __init__(self,website='default'):
        self.website=website
        self.cookies_db=RedisClient('cookies',self.website)
        self.accounts_db=RedisClient('accounts',self.website)
        self.init_browser()

    #关闭Browser
    def __del__(self):
        try:
            print('Closing Browser')
            self.browser.close()
            del self.browser
        except TypeError:
            print('Browser not opened')

    #利用Browser参数初始化全局浏览器供模拟登录使用
    def init_browser(self):
        if BROWSER_TYPE=='PhantomJS':
            caps=DesiredCapabilities.PHANTOMJS
            caps[
                'phantomjs.page.settings.userAgent']='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36' \
                                                     ' (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
            self.browser=webdriver.PhantomJS(desired_capabilities=caps)
            self.browser.set_window_size(1400, 500)
        if BROWSER_TYPE=='Chrome':
            chrome_options=webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            self.browser=webdriver.Chrome(chrome_options=chrome_options)


    #新生成cookies,子类需要重写
    def new_cookies(self,username,password):
        raise NotImplementedError


    #处理cookies,  self.browser.get_cookies()此方法获得的cookies是个列表,其中每个元素都是个字典,我们需要取出字典中的name和value键所对应的值组成新的字典
    def process_cookies(self,cookies):
        dict={}
        for cookie in cookies:
            dict[cookie['name']]=cookie['value']
        return dict


    #运行,得到所有账户,然后顺次模拟登陆
    def run(self):
        cookies_usernames=self.cookies_db.usernames()
        accounts_usernames=self.accounts_db.usernames()
        for username in accounts_usernames:
            if not username in cookies_usernames:
                password=self.accounts_db.get(username)
                print('正在生成Cookies','账号',username,'密码',password)
                result=self.new_cookies(username,password)
                #成功获取
                if result.get('status')==1:
                    cookies=self.process_cookies(result.get('content'))
                    print('成功获取到Cookies',cookies)
                    if self.cookies_db.set(username,json.dumps(cookies)):
                        print('成功保存Cookies')
                #密码错误,移除账号
                elif result.get('status')==2:
                    print(result.get('content'))
                    if self.accounts_db.delete(username):
                        print('成功删除账号')
                else:
                    print(result.get('content'))
            else:
                print('所有账号都已成功获取Cookies')


#对接微博cookies的子类,如需扩展其他站点,可再增加子类
class WeiboCookiesGenerator(CookiesGenerator):
    #初始化操作
    def __init__(self,website='weibo'):
        CookiesGenerator.__init__(self,website)
        self.website=website

    #不同站点有不同的生成cookies的方法
    def new_cookies(self,username,password):
        return WeiboCookies(username,password,self.browser).main()


if __name__=='__main__':
    generator=WeiboCookiesGenerator()
    generator.run()


