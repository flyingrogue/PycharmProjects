#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import requests
import time
import os
import sys

def get_page():
    url='https://box.maoyan.com/promovie/api/box/second.json'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 '
                 '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'
    }
    try:
        res=requests.get(url,headers=headers)
        if res.status_code==200:
            return res.json()
        else:
            return None
    except requests.ConnectionError as e:
        print('Error',e.args)

def parse_page(json):
    if json:
        data=json.get('data')
        for item in data.get('list'):
            piaofang={}
            piaofang['avgSeatView']=item.get('avgSeatView')
            piaofang['avgShowView']=item.get('avgShowView')
            piaofang['avgViewBox']=item.get('avgViewBox')
            piaofang['boxInfo']=item.get('boxInfo')
            piaofang['boxRate']=item.get('boxRate')
            piaofang['movieName']=item.get('movieName')
            piaofang['releaseInfo']=item.get('releaseInfo')
            piaofang['showRate']=item.get('showRate')
            piaofang['showInfo']=item.get('showInfo')
            piaofang['sumBoxInfo']=item.get('sumBoxInfo')
            yield piaofang

if __name__=='__main__':
    while True:
        json=get_page()
        results=parse_page(json)
        os.system('cls')
        print(json.get('data')['updateInfo'])
        print('今日总票房:{}{}'.format(json.get('data')['totalBox'],json.get('data')['totalBoxUnit']))
        line='-'*150
        print(line)
        print('电影名称\t综合票房(万)\t票房占比\t拍片场次\t排片占比\t场均人次\t上座率\t平均票价\t累积总票房\t上映天数')
        print(line)
        for result in results:
            print(result['movieName'][:7].ljust(8)+'\t'+
                  result['boxInfo'][:8].rjust(8)+'\t'+
                  result['boxRate'][:8].rjust(8)+'\t'+
                  result['showInfo'][:8].rjust(8)+'\t'+
                  result['showRate'][:8].rjust(8)+'\t'+
                  result['avgShowView'][:8].rjust(8)+'\t'+
                  result['avgSeatView'][:8].rjust(8)+'\t'+
                  result['avgViewBox'][:8].rjust(8)+'\t'+
                  result['sumBoxInfo'][:8].rjust(8)+'\t'+
                  result['releaseInfo'][:8])
        time.sleep(4)



