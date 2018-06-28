# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SuningItem(scrapy.Item):
    """
    这里是放防虫item字典里面所用的key约束
    """
    b_cate = scrapy.Field()
    s_href = scrapy.Field()
    s_cate = scrapy.Field()
    book_name = scrapy.Field()
    book_img = scrapy.Field()
    book_author = scrapy.Field()
    book_press = scrapy.Field()
    book_desc = scrapy.Field()
    book_href = scrapy.Field()
    book_price = scrapy.Field()