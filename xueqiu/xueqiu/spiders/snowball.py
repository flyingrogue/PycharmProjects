# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import json
from xueqiu.items import StatusItem

class SnowballSpider(scrapy.Spider):
    name = 'snowball'
    allowed_domains = ['xueqiu.com']

    stock_url='https://xueqiu.com/S/{code}'
    fan_url='https://xueqiu.com/S/{code}/follows?page={page}'
    user_url='https://xueqiu.com/v4/statuses/user_timeline.json?page={page}&user_id={uid}'
    start_stocks=['','','']

    def start_requests(self):
        for code in self.start_stocks:
            yield Request(self.fan_url.format(code=code,page=1),callback=self.parse_fans,meta={'page':1,'code':code})


    #解析粉丝列表
    def parse_fans(self, response):
        globals = {
            'true': 0,
            'false': 1,
            'null': 0
        }
        pattern = re.compile('followers":(.*),"an', re.S)
        result = re.findall(pattern, response.text)
        if result:
            lis = eval(result[0], globals)
            for li in lis:
                uid=li['id']
                yield Request(self.user_url.format(uid=uid,page=1), callback=self.parse_user,meta={'page':1,'uid':uid})

        #下一页粉丝
        code = response.meta.get('code')
        page = response.meta.get('page') + 1
        yield Request(self.fan_url.format(code=code,page=page),callback=self.parse_fans,meta={'page':page,'code':code})

    #解析用户帖子列表
    def parse_user(self,response):
        result = json.loads(response.text)
        statuses = result.get('statuses')
        if result.get('statuses'):
            status_item=StatusItem()
            for status in statuses:
                status_item['user_id']=status.get('user_id')
                status_item['status_id']=status.get('id')
                status_item['content']=status.get('text')
                status_item['retweet_count']=status.get('retweet_count')
                status_item['reply_count']=status.get('reply_coun')
                status_item['like_count']=status.get('like_count')
                yield status_item

        #下一页帖子
        uid = response.meta.get('uid')
        page = response.meta.get('page') + 1
        yield Request(self.user_url.format(uid=uid, page=page), callback=self.parse_user,meta={'uid': uid, 'page': page})





