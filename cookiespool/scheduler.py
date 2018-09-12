#!/usr/bin/env python
# _*_ coding:utf-8 _*_


import time
from multiprocessing import Process
from cookiespool.config import *
from cookiespool.generator import *
from cookiespool.tester import *
from cookiespool.api import app


class Scheduler(object):
    @staticmethod
    def valid_cookie(cycle=CYCLE):
        while True:
            print('Cookies检测进程开始运行')
            try:
                for website,cls in TESTER_MAP.items():
                    tester=eval(cls + '(website="' + website + '")')
                    tester.run()
                    print('Cookies检测完成')
                    del tester
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def generate_cookie(cycle=CYCLE):
        while True:
            print('Cookies生成进程开始运行')
            try:
                for website,cls in GENERATOR_MAP.items():
                    generator=eval(cls + '(website="' + website + '")')
                    generator.run()
                    print('Cookies生成完成')
                    del generator
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def api():
        print('API接口开始运行')
        app.run(host=API_HOST,port=API_PORT)


    def run(self):
        if API_PROCESS:
            api_process=Process(target=Scheduler.api)
            api_process.start()

        if GENERATOR_PROCESS:
            generator_process=Process(target=Scheduler.generate_cookie)
            generator_process.start()

        if VALID_PROCESS:
            valid_process=Process(target=Scheduler.valid_cookie)
            valid_process.start()


if __name__=='__main__':
    s=Scheduler()
    s.run()

