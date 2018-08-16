#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import requests
import json
from requests.exceptions import RequestException
from lxml import etree
import time
import pymongo

def get_page(offest):
    url='http://maoyan.com/board/4?offset='+str(offest)
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 '
                     '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    try:
       res=requests.get(url,headers=headers)
       if res.status_code==200:
           return res.text
       return None
    except RequestException:
        return None

def parse_page(page):
    html=etree.HTML(page)
    index=html.xpath('//*[@id="app"]/div/div/div[1]/dl/dd/i/text()')
    title=html.xpath('//*[@id="app"]/div/div/div[1]/dl/dd/div/div/div[1]/p[1]/a/text()')
    actor=html.xpath('//*[@id="app"]/div/div/div[1]/dl/dd/div/div/div[1]/p[2]/text()')
    time=html.xpath('//*[@id="app"]/div/div/div[1]/dl/dd/div/div/div[1]/p[3]/text()')
    href=html.xpath('//*[@id="app"]/div/div/div[1]/dl/dd/div/div/div[1]/p[1]/a/@href')
    for i in range(10):
        yield {
            'index':index[i],
            'title':title[i],
            'actor':actor[i].strip()[3:],
            'time':time[i][5:],
            'href':'http://maoyan.com'+href[i]
        }

def write_file(content):
    with open('maoyantop100.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')

def open_mongodb():
    client=pymongo.MongoClient(host='localhost',port=27017)
    db=client.maoyan
    collection=db.top100
    return collection

def main():
    collection=open_mongodb()
    for i in range(10):
        page=get_page(i*10)
        #collection.insert_many(list(parse_page(page)))
        for item in parse_page(page):
            print(item)
            write_file(item)
            collection.insert_one(item)
        time.sleep(1)

if __name__=='__main__':
    main()




