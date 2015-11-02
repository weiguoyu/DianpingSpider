# -*- coding: utf-8 -*-

import scrapy
from dianping.items import DianpingItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class XingzhengquSpider(CrawlSpider):
    name = "DianpingSpider"
    allowed_domains = ["dianping.com"]
    shops_count = 0
    categary = "早餐"
    start_urls = ["http://www.dianping.com/citylist/citylist?citypage=1"]
    rules = (
        # rule for city
        Rule(
            LinkExtractor(
                restrict_xpaths='///div[@class="section"]//'
                'a[contains(@onclick, "pageTracker")]'
            ),
            callback='parse_city'
        ),
        # rule for xingzhengqu
        Rule(
            LinkExtractor(restrict_xpaths='//div[@id="region-nav-sub"]//a'),
            follow=True
        ),
        # rule for local area belongs to corresponding xingzhenqu
        Rule(
            LinkExtractor(restrict_xpaths='//div[@id="region-nav-sub"]//a'),
            follow=True
        ),
        # rule for page index in each local area
        Rule(
            LinkExtractor(restrict_xpaths='//div[@class="page"]//a'),
            follow=True
        ),
        # rule for shops in each page
        Rule(
            LinkExtractor(
                restrict_xpaths=
                '//div[@class="shop-list J_shop-list shop-all-list"]'
                '//a[@data-hippo-type="shop"]'
            ),
            follow=True,
            callback='parse_dianping'
        ),
    )

    def parse_city(self, response):
        city_id = response.xpath(
            '//div[@class="search-bar"]/input/@data-s-cityid').extract()[0]
        cate_id = response.xpath(
            '//div[@class="search-bar"]/input/@data-s-cateid').extract()[0]
        cate = self.categary
        url = "http://www.dianping.com/search/keyword/{0}/{1}_{2}".format(
            city_id,cate_id,cate)
        print url
        yield scrapy.Request(url)


    def parse_dianping(self, response):
        item = DianpingItem()
        item['shop_name'] = response.xpath(
            '//h1[@class="shop-name"]//text()').extract()[0].strip()
        item['shop_address'] = response.xpath(
            '//div[@class="expand-info address"]//'
            'span[@itemprop="street-address"]/@title').extract()[0]
        lng_atr = response.xpath('//div[@id="aside"]/script/text()')\
            .re(r"lng:(\d*.\d*),lat:(\d*.\d*)")
        item['shop_longitude'], item['shop_latitude'] = lng_atr
        item['shop_city'] = response.xpath(
            '//a[@class="city J-city"]//text()').extract()[0].strip()
        item['shop_region'] = response.xpath(
            '//span[@itemprop="locality region"]//text()').extract()[0].strip()

        self.shops_count += 1
        print "%d shops are crawled." %self.shops_count
        yield item
