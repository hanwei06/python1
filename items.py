# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Recruit51JobItem(scrapy.Item):


    # 网站地址
    link = scrapy.Field()

    # 内容
    content = scrapy.Field()

    # 标题
    title = scrapy.Field()

    # 发布时间
    fbDate = scrapy.Field()

    # 数据来源
    source = scrapy.Field()