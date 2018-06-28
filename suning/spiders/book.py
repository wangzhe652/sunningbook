# -*- coding: utf-8 -*-
import scrapy
import re
from copy import deepcopy
from ..items import SuningItem


class SuningSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['suning.com']
    start_urls = ['http://snbook.suning.com/web/trd-fl/999999/0.htm']

    def parse(self, response):
        # 1.大分类分组 大标题
        li_list = response.xpath("//ul[@class='ulwrap']/li")
        for li in li_list:
            item = SuningItem()
            item["b_cate"] = li.xpath("./div[1]/a/text()").extract_first()  # 获取每一个大标题 父标题
            # 2.小分类分组
            a_list = li.xpath("./div[2]/a")  # 获取每一个小标题
            for a in a_list:
                item["s_href"] = a.xpath("./@href").extract_first()  # 获取每一个小标题的链接
                item["s_cate"] = a.xpath("./text()").extract_first()  # 获取每一个小标题的标题名称
                if item["s_href"] is not None:
                    # 这里是对子标题的链接进行判断 不为空就进行获取拼接完整的url链接
                    item["s_href"] = "http://snbook.suning.com/" + item["s_href"]
                    # 把获取到的子标题的链接丢给下一个图标列表函数进行处理，并把字典传过去，这里的字典用的是深拷贝因为防止多次写入冲突
                    yield scrapy.Request(
                        item["s_href"],
                        callback=self.parse_book_list,
                        meta={"item": deepcopy(item)}
                    )

    def parse_book_list(self, response):
        """
        这里是对子标题的图书列表进行获取，补货每一个图书的信息
        """
        item = deepcopy(response.meta["item"])  # 接收一下从上面传过来的字典，进行数据的续写
        # 图书列表页分组 所有的列表捕获
        li_list = response.xpath("//div[@class='filtrate-books list-filtrate-books']/ul/li")
        for li in li_list:
            item["book_name"] = li.xpath(".//div[@class='book-title']/a/@title").extract_first()  # 图书的名字
            item["book_img"] = li.xpath(".//div[@class='book-img']//img/@src").extract_first()  # 图书url链接
            # 这里进行判断因为有的图书的url在src 或者在src2里面 就要进行判断了
            if item["book_img"] is None:
                item["book_img"] = li.xpath(".//div[@class='book-img']//img/@src2").extract_first()
            item["book_author"] = li.xpath(".//div[@class='book-author']/a/text()").extract_first()  # 图书的作者
            item["book_press"] = li.xpath(".//div[@class='book-publish']/a/text()").extract_first()  # 图书的出版社
            item["book_desc"] = li.xpath(".//div[@class='book-descrip c6']/text()").extract_first()  # 图书的简介
            item["book_href"] = li.xpath(".//div[@class='book-title']/a/@href").extract_first()  # 图书的链接
            # 接下来发送一个request请求把获取到的图书的链接丢给，图书详情处理方法，传递的依旧是深拷贝
            yield scrapy.Request(
                item["book_href"],
                callback=self.parse_book_detail,
                meta={"item": deepcopy(item)}
            )

        # 翻页用正则表达式获取到 代码里面的总页数 以及当前页面
        page_count = int(re.findall("var pagecount=(.*?);", response.body.decode())[0])
        current_page = int(re.findall("var currentPage=(.*?);", response.body.decode())[0])
        if current_page < page_count:
            next_url = item["s_href"] + "?pageNumber={}&sort=0".format(current_page + 1)
            yield scrapy.Request(
                next_url,
                callback=self.parse_book_list,
                meta={"item": response.meta["item"]}
            )

    def parse_book_detail(self, response):
        """这里是专门用来处理图书详情列表的方法"""
        item = response.meta["item"]  # 接收传递的item字典 进行续写
        item["book_price"] = re.findall("\"bp\":'(.*?)',", response.body.decode())  # 使用正则表达式获取图书的价格
        item["book_price"] = item["book_price"][0] if len(item["book_price"]) > 0 else None
        yield item
