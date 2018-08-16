#!/usr/bin/env python
# _*_ coding:utf-8 _*_


import redis
from pickle import dumps,loads
from request import WeixinRequest
from config import *

class RedisQueue():
    #初始化Redis
    def __init__(self):
        self.db=redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT,password=REDIS_PASSWORD)

    #向队列添加序列化后的Request
    def add(self,request):
        if isinstance(request,WeixinRequest):
            return self.db.rpush(REDIS_KEY,dumps(request))
        return False

    #取出下一个Request并反序列化
    def pop(self):
        if self.db.llen(REDIS_KEY):
            return loads(self.db.lpop(REDIS_KEY))
        return False

    def empty(self):
        return self.db.llen(REDIS_KEY)==0
