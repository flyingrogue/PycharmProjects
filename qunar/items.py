# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QunarItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection=table='travel'
    title=scrapy.Field()
    date=scrapy.Field()
    howlong=scrapy.Field()
    howmuch=scrapy.Field()
    text=scrapy.Field()
    url=scrapy.Field()
