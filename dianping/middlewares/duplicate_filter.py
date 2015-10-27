#!/usr/bin/env python
# encoding: utf-8

from scrapy.dupefilters import RFPDupeFilter
from pybloomfilter import BloomFilter
import os

PATH = os.path.dirname(os.path.join(os.path.pardir, os.path.dirname(__file__)))
print PATH
FILTER_PATH = os.path.abspath(os.path.join(PATH, 'filter/url_filter.bloom'))
print FILTER_PATH


class DuplicateFilter(RFPDupeFilter):
    """
    A dupe filter for url
    """

    url_filter = BloomFilter(10000, 0.001, FILTER_PATH)

    def request_seen(self, request):
        return self.url_filter.add(request.url)
