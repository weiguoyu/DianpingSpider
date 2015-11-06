#!/bin/bash

export PATH=$PATH:/usr/local/bin

cd /Users/jason/dev/DianpingSpider

source venv/bin/activate

scrapy crawl IpSpider

cat dianping/ip.txt

