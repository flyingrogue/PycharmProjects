#!/usr/bin/env python
# _*_ coding:utf-8 _*_

'''
接口模块:需要用API来提供对外服务的接口
'''

from flask import Flask,g
from proxypool.db import RedisClient


__all__=['app']
app=Flask(__name__)

def get_conn():
    if not hasattr(g,'redis'):
        g.redis=RedisClient()
        return g.redis

@app.route('/')
def index():
    return '<h2>Welcome to Proxy Pool System</h2>'

#随机获取可用代理
@app.route('/random')
def get_proxy():
    conn=get_conn()
    return conn.random()

#获取代理池总量
@app.route('/count')
def get_counts():
    conn=get_conn()
    return str(conn.count())

if __name__=='__main__':
    app.run(host='127.0.0.1',port=5000)