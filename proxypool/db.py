#!/usr/bin/env python
# _*_ coding:utf-8 _*_

'''
存储模块: 负责存储抓取下来的代理
'''

from settings import MAX_SCORE,MIN_SCORE,INITIAL_SCORE
from settings import REDIS_HOST,REDIS_PORT,REDIS_PASSWORD,REDIS_KEY
from error import PoolEmptyError
import redis
import re
from random import choice

#这个类可以用来操作Redis的有序集合
class RedisClient(object):
    #初始化
    def __init__(self,host=REDIS_HOST,port=REDIS_PORT,password=REDIS_PASSWORD):
        self.db=redis.StrictRedis(host=host,port=port,password=password,decode_responses=True)

    #添加代理,设置分数为最高
    def add(self,proxy,score=INITIAL_SCORE):
        if not re.match('\d+\.\d+\.\d+\.\d+:\d+',proxy):
            return
        if not self.db.zscore(REDIS_KEY,proxy):
            self.db.zadd(REDIS_KEY,score,proxy)

    #随机获取有效代理
    def random(self):
        result=self.db.zrangebyscore(REDIS_KEY,MAX_SCORE,MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result=self.db.zrevrange(REDIS_KEY,0,100)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    #代理值减一分,分数小于最小值则删除
    def decrease(self,proxy):
        score=self.db.zscore(REDIS_KEY,proxy)
        if score and score>MIN_SCORE:
            print('代理',proxy,'当前分数',score,'减1')
            return self.db.zincrby(REDIS_KEY,proxy,-1)
        else:
            print('代理',proxy,'当前分数',score,'移除')
            return self.db.zrem(REDIS_KEY,proxy)

    #判断是否存在
    def exists(self,proxy):
        return not self.db.zscore(REDIS_KEY,proxy)==None

    #将代理设置为最高分
    def max(self,proxy):
        print('代理',proxy,'可用,设置为',MAX_SCORE)
        return self.db.zadd(REDIS_KEY,MAX_SCORE,proxy)

    #获取数量
    def count(self):
        return self.db.zcard(REDIS_KEY)

    #获取全部代理
    def all(self):
        return self.db.zrangebyscore(REDIS_KEY,MIN_SCORE,MAX_SCORE)

    #批量获取
    def batch(self,start,stop):
        return self.db.zrevrange(REDIS_KEY,start,stop - 1)


if __name__=='__main__':
    coon=RedisClient
    result=coon.batch(66,77)
    print(result)




