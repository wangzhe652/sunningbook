# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re


class SuningPipeline(object):
    """
    这里是接收book.py里面的parse里面yield生成器 生成的值 用来管道进行处理
    """

    def process_item(self, item, spider):
        print(item)
        return item
