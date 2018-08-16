# -*- coding: utf-8 -*-
import scrapy
from qunar.items import QunarItem
from qunar.settings import MAX_PAGE

class TravelSpider(scrapy.Spider):
    name = 'travel'
    allowed_domains = ['travel.qunar.com']
    start_urls = ['http://travel.qunar.com']

    count=1
    def start_requests(self):
        url='http://travel.qunar.com/travelbook/list.htm'
        yield scrapy.Request(url,callback=self.index_parse)

    def index_parse(self, response):
        hrefs=response.css('.list_item::attr(data-url)').extract()
        for href in hrefs:
            url='http://travel.qunar.com'+href
            yield scrapy.Request(url,callback=self.detail_parse)
        next=response.css('.next::attr(href)').extract_first()
        if self.count<MAX_PAGE:
            if next:
                self.count+=1
                url='http:'+next
                yield scrapy.Request(url,callback=self.index_parse)

    def detail_parse(self,response):
        item=QunarItem()
        item['title']=response.css('#booktitle::text').extract_first()
        item['date']=response.css('.when .data::text').extract_first()
        item['howlong']=response.css('.howlong .data::text').extract_first()
        item['howmuch']=response.css('.howmuch .data::text').extract_first()
        item['text']=''.join(response.xpath('//*[@id="tpl_1"]//text()').extract())
        item['url']=response.url
        yield item




