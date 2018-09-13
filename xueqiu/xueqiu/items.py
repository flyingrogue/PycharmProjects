# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StatusItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection='statuses'
    user_id=scrapy.Field()
    status_id=scrapy.Field()
    content=scrapy.Field()
    retweet_count=scrapy.Field()
    reply_count=scrapy.Field()
    like_count=scrapy.Field()
