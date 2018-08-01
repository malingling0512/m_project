# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZuofanScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

#zuofan 数据
class ZuofanItem(scrapy.Item):
    title=scrapy.Field()
    time_new = scrapy.Field()
    cook = scrapy.Field()
    source = scrapy.Field()
    look_num = scrapy.Field()
    abstract = scrapy.Field()
    str_yl = scrapy.Field()
    str_tl = scrapy.Field()
    str_jq = scrapy.Field()
    str_bz = scrapy.Field()
    titleimage = scrapy.Field()
