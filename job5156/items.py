# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field,Item


class JobItem(Item):
    # define the fields for your item here like:
    # name = Field()
    posname=Field()
    posdesc=Field()
    degree=Field()
    experience=Field()
    address=Field()
