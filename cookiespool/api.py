#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import json
from flask import Flask,g
from cookiespool.db import RedisClient
from cookiespool.config import *


__all__=['app']

app=Flask(__name__)

@app.route('/')
def index():
    return '<h2>Welcome to Cookie Pool System</h2>'

#获取存储模块的连接
def get_conn():
    for website in GENERATOR_MAP:
        if not hasattr(g,website):
            setattr(g,website + '_cookies',eval('RedisClient' + '("cookies", "' + website + '")'))
            setattr(g,website + '_accounts',eval('RedisClient' + '("accounts", "' + website + '")'))
    return g

#获取随机的Cookie, 访问地址如 /weibo/random
@app.route('/<website>/random')
def random(website):
    g=get_conn()
    cookies=getattr(g,website + '_cookies').random()
    return cookies

#添加用户, 访问地址如 /weibo/add/user/password
@app.route('/<website>/add/<username>/<password>')
def add(website,username,password):
    g=get_conn()
    getattr(g,website + '_accounts').set(username,password)
    return json.dumps({'status':'1'})

#获取cookies总数
@app.route('/<website>/count')
def count(website):
    g=get_conn()
    count=getattr(g,website + '_cookies').count()
    return json.dumps({'status':'1','count':count})


if __name__=='__main__':
    app.run(host='127.0.0.1',port=5555)