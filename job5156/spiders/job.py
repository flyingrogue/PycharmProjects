# -*- coding: utf-8 -*-
from scrapy import Spider,Request
from urllib.parse import urlencode
import json
from job5156.items import JobItem

class JobSpider(Spider):
    name = 'job'
    allowed_domains = ['www.job5156.com']
    start_urls = ['http://www.job5156.com/']

    def start_requests(self):
        base_url='http://www.job5156.com/s/result/ajax.json?'
        data={'keyword':self.settings.get('KEYWORD'),'keywordType':0,'locationList':self.settings.get('LOCATION'),'sortB':0}
        for page in range(1,self.settings.get('MAX_PAGE')+1):
            data['pageNo']=page
            url=base_url+urlencode(data)
            yield Request(url,callback=self.index_parse)


    def index_parse(self, response):
        result=json.loads(response.text)
        infos=result.get('page').get('items')
        for info in infos:
            href=info.get('posDetailUrl')
            url='http://www.job5156.com'+href
            yield Request(url,callback=self.detail_parse)


    def detail_parse(self,response):
        item=JobItem()
        item['posname']=response.css('.pos_wrap .pos_name::text').extract_first()
        item['posdesc']=response.css('.pos_describle_content pre::text').extract_first()
        item['degree']=response.css('.requirements li:first-child p::text').extract_first()
        item['experience']=response.css('.requirements li:nth-child(2) p::text').extract_first()
        item['address']=response.css('.requirements li:nth-child(3) p::text').extract_first()
        yield item



