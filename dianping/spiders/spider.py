#!/usr/bin/env python
# encoding: utf-8

import scrapy
from scrapy.selector import Selector
from dianping.items import DianpingItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

BASE_URL = 'www.dianping.com'

class XingzhengquSpider(CrawlSpider):
    name = "DianpingSpider"
    allowed_domains = ["dianping.com"]
    shops_count = 0
    #  start_urls = ["http://www.dianping.com/search/keyword/1/0_咖喱米粉店"]
    start_urls = ["http://www.dianping.com/search/keyword/1/0_早餐面馆"]
    rules = (
            # rule for xingzhengqu
            Rule(LinkExtractor(allow=(r'\w*'), restrict_xpaths='//div[@class="nav-category nav-tabs"]'
                '//div[@class="nc-contain"]//div[@id="J_nt_items"]'
                '//div[@id="region-nav"]//a'), follow=True),
            # rule for local area belongs to corresponding xingzhenqu
            Rule(LinkExtractor(allow=(r'\w*'), restrict_xpaths='//div[@class="nav-category nav-tabs"]'
                '//div[@class="nc-contain"]//div[@id="J_nt_items"]'
                '//div[@id="region-nav-sub"]//a'), follow=True),
            # rule for page index in each local area
            Rule(LinkExtractor(allow=(r'\w*'), restrict_xpaths='//div[@class="page"]//a'), follow=True),
            # rule for shops in each page
            Rule(LinkExtractor(allow=(r'\/shop\/\d*$'), restrict_xpaths='//li//div//a'
                '[@target="_blank"]'), follow=True, callback='parse_dianping'),
            )

    #  def test(self, response):
        #  print response.request.headers
        #  print response.request

    def parse_dianping(self, response):

        item = DianpingItem()
        res = Selector(response)

        item['shop_name'] = res.xpath('//div[@class="main"]'
                '//div//h1/text()').re('\S[^\b]*')[0].strip()
        item['shop_region'] = res.xpath('//a//span[@itemprop='
                '"locality region"]/text()').extract()[0].strip()
        item['shop_address'] = res.xpath('//div[@class="expand-info address"]'
                '//span[@class="item"]/@title').extract()[0].strip()
        item['shop_longitude'], item['shop_latitude'] = res.xpath('//script')\
                .re(r'\{lng\:(?P<lng>[\d\.]*)\,lat\:(?P<lat>[\d\.]*)\}')
        item['shop_city'] = res.xpath('//a[@class="city J-city"]//text()').extract()[0].strip()
        self.shops_count += 1
        print "%d shops are crawled." %self.shops_count
        #  print response.headers
        yield item
