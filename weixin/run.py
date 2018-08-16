#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from spider import Spider

#入口
def run():
    spider=Spider()
    spider.start()
    spider.schedule()

if __name__=='__main__':
    run()
