#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from settings import *
from multiprocessing import Process
from api import app
from getter import Getter
from tester import Tester
import time

class Scheduler():
    #定时获取代理
    @staticmethod
    def schedule_getter(cycle=GETTER_CYCLE):
        getter=Getter()
        while True:
            print('开始抓取代理')
            getter.run()
            time.sleep(cycle)

    #定时测试代理
    @staticmethod
    def schedule_tester(cycle=TESTER_CYCLE):
        tester=Tester()
        while True:
            print('测试器开始运行')
            tester.run()
            time.sleep(cycle)

    #开启API
    @staticmethod
    def schedule_api():
        print('API接口开始运行')
        app.run(API_HOST,API_PORT)


    def run(self):
        print('代理池开始运行')
        if GETTER_ENABLED:
            getter_process=Process(target=self.schedule_getter)
            getter_process.start()

        if TESTER_ENABLED:
            tester_process=Process(target=self.schedule_tester)
            tester_process.start()

        if API_ENABLED:
            api_process=Process(target=self.schedule_api)
            api_process.start()


if __name__=='__main__':
    s=Scheduler()
    s.run()