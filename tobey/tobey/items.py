# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class AppItem(Item):
    title = Field()  # 标题
    link = Field()   # 来源
    content = Field() # 正文
    category = Field() # 分类[]
    tag = Field()      # 标签[]
    thumbnail_src = Field() # 标题图片
    publish_date = Field() # 发布时间 "2012-10-10 11:30"
