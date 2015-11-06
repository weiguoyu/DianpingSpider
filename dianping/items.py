# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DianpingItem(scrapy.Item):
    shop_name = scrapy.Field()
    shop_address = scrapy.Field()
    shop_region = scrapy.Field()
    shop_city = scrapy.Field()
    shop_latitude = scrapy.Field()
    shop_longitude = scrapy.Field()


class IpProxyItem(scrapy.Item):
    agent = scrapy.Field()
