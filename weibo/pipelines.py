# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from weibo.items import UserItem,WeiboItem,UserRelationItem
import re
import time
import pymongo

class WeiboPipeline():
    def parse_time(self,date):
        if re.match('刚刚',date):
            date=time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
        if re.match('\d+分钟前',date):
            minute=re.match('(\d+)',date).group(1)
            date=time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()-float(minute)*60))
        if re.match('\d+小时前',date):
            hour=re.match('(\d+)',date).group(1)
            date=time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()-float(hour)*60*60))
        if re.match('昨天.*',date):
            date=re.match('昨天(.*)',date).group(1).strip()
            date=time.strftime('%Y-%m-%d',time.localtime()-24*60*60)+''+date
        if re.match('\d{2}-\d{2}',date):
            date=time.strftime('%Y-',time.localtime())+date+' 00:00'

    def process_item(self,item,spider):
        if isinstance(item,WeiboItem):
            if item.get('created_at'):
                item['created_at']=item['created_at'].strip()
                item['created_at']=self.parse_time(item.get('created_at'))
        return item

class TimePipeline():
    def process_item(self,item,spider):
        if isinstance(item,UserItem) or isinstance(item,WeiboItem):
            now=time.strftime('%Y-%m-%d %H:%M',time.localtime())
            item['crawled_at']=now
        return item


class MongoPipeline(object):
    def __init__(self,mongo_url,mongo_db):
        self.mongo_url=mongo_url
        self.mongo_db=mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self,spider):
        self.client=pymongo.MongoClient(host=self.mongo_url)
        self.db=self.client[self.mongo_db]
        self.db[UserItem.collection].create_index([('id',pymongo.ASCENDING)])
        self.db[WeiboItem.collection].create_index([('id',pymongo.ASCENDING)])

    def close_spider(self,spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item,UserItem) or isinstance(item,WeiboItem):
            self.db[item.collection].update({'id':item.get('id')},{'$set':item},True)
        if isinstance(item,UserRelationItem):
            self.db[item.collection].update(
                {'id':item.get('id')},
                {'$addToSet':
                    {
                        'follows':{'$each':item['follows']},
                         'fans':{'$each':item['fans']}
                    }
                },True)
        return item
