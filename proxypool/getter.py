#!/usr/bin/env python
# _*_ coding:utf-8 _*_

'''
获取模块的启动器: 动态调用所有以crawl开头的方法,然后获取抓取到的代理,将其送入数据库存储
'''
from proxypool.db import RedisClient
from proxypool.crawler import Crawler
from proxypool.settings import POOL_UPPER_THRESHOLD

class Getter():
    def __init__(self):
        self.redis=RedisClient()
        self.crawler=Crawler()

    #判断是否达到了代理池限制
    def is_over_threshold(self):
        if self.redis.count() >=POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        print('获取器开始执行')
        if not self.is_over_threshold():
            for index in range(self.crawler.__CrawlFuncCount__):
                callback=self.crawler.__CrawlFunc__[index]
                proxies=self.crawler.get_proxies(callback)
                for proxy in proxies:
                    self.redis.add(proxy)


