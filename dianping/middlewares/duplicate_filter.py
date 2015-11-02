# -*- coding: utf-8 -*-

from scrapy.dupefilters import RFPDupeFilter
from pybloomfilter import BloomFilter
from scrapy.utils.request import request_fingerprint
import os

PATH = os.path.dirname(os.path.join(os.path.pardir, os.path.dirname(__file__)))
FILTER_PATH = os.path.abspath(os.path.join(PATH, 'filter/url_filter.bloom'))


class DuplicateFilter(RFPDupeFilter):
    """
    A dupe filter for url
    """
    def __init__(self, path=FILTER_PATH, debug=False):
        if os.path.exists(FILTER_PATH):
            self.url_filter = BloomFilter.open(FILTER_PATH)
        else:
            print "created a new bloom filter. "
            self.url_filter = BloomFilter(100000, 0.00001, FILTER_PATH)
        super(DuplicateFilter, self).__init__(path, debug)

    def request_fingerprint(self, request):
        return request_fingerprint(request)

    def request_seen(self, request):
        fp = self.request_fingerprint(request)
        if self.url_filter.add(fp):
            print ">" * 5 + "filtered " + request.url + "<" * 5
            return True

    def close(self, reason):
        self.url_filter = None
