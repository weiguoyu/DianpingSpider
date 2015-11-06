# -*- coding: utf-8 -*-

from scrapy.downloadermiddlewares.retry import RetryMiddleware
import logging
import random


logger = logging.getLogger(__name__)
PROXY_PORT = {}
with open("ip.txt", "r") as ip_pool:
    for lines in ip_pool.readlines():
        ip, port = lines.split(":")
        PROXY_PORT.update({ip: port})
print PROXY_PORT


class CustomRetryMiddleware(RetryMiddleware):
    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1
        print PROXY_PORT
        if retries <= self.max_retry_times:
            logger.debug(
                "Retrying %(request)s (failed %(retries)d times): %(reason)s",
                {
                    'request': request,
                    'retries': retries,
                    'reason': reason
                },
                extra={'spider': spider}
            )
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust
            print ">>>>>>>>>>>>>>>>>>>>>>>>>proxy<<<<<<<<<<<<<<<<<<<<<", PROXY_PORT
            ip = random.choice(PROXY_PORT.keys())
            port = PROXY_PORT[ip]
            retryreq.meta['proxy'] = "http://" + ip + ":" + port
            return retryreq
        else:
            logger.debug(
                "Gave up retrying %(request)s (failed %(retries)d times): "
                "%(reason)s",
                {
                    'request': request,
                    'retries': retries,
                    'reason': reason
                },
                extra={'spider': spider}
            )
