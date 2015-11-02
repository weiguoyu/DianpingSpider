# -*- coding: utf-8 -*-

from scrapy.downloadermiddlewares.retry import RetryMiddleware
import logging
import random


logger = logging.getLogger(__name__)
PROXY_PORT = {
    "121.32.52.10": "9999",
    "111.12.117.68": "8080",
    "218.95.81.102": "9000",
    "182.205.140.84": "80",
    "182.205.117.103": "3128",
    "49.93.26.51": "3128",
    "49.94.14.167": "3128",
    "27.46.21.24": "8888",
    "163.125.125.16": "9999",
    "113.125.59.59": "80",
    }


class CustomRetryMiddleware(RetryMiddleware):
    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1

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