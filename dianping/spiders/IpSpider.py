#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider
from dianping.items import IpProxyItem
from requests.exceptions import RequestException
import requests


class IpSpider(CrawlSpider):
    """Spider used to maintain ip agents"""
    name = "IpSpider"
    #  allowed_domains = ["kuaidaili.com"]
    start_urls = [
            "http://www.kuaidaili.com",
            "http://www.xicidaili.com"
            ]

    def parse(self, response):
        res = IpProxyItem()
        ip = response.xpath('//body//div//tr//td')\
                .re(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
        # for the problem of xpath, i have to use ugly re like this
        port = response.xpath('//body//div//tr')\
                .re('\<td\>(?P<port>\d*)\<\/td\>')
        res['agent'] = dict(filter(self.test_send_request, zip(ip, port)))
        yield res

    @staticmethod
    def test_send_request(agent):
        """method used to test whether the agent is qualified.
        agent: <tuple> (ip, proxy)"""
        ip, port = agent[0], agent[1]
        proxies = {"http": "http://" + ip + ':' + port}
        url = "http://www.baidu.com"
        try:
            response = requests.get(url, proxies=proxies, timeout=0.1)
        except RequestException as error:
            print "proxies: {} failed".format(proxies)
        else:
            return response.ok
