# -*- coding: utf-8 -*-

"""
Importing base64 library because we'll need it ONLY in case
if the proxy we are going to use requires authentication
"""
import random


PROXY_PORT = {}
with open('ip.txt', 'r') as ip_pool:
    for lines in ip_pool.readlines():
        ip, port = lines.split(':')
        PROXY_PORT.update({ip: port})


# Start your middleware class
class ProxyMiddleware(object):
    # overwrite process request

    def process_request(self, request, spider):
        # Set the location of the proxy
        ip = random.choice(PROXY_PORT.keys())
        request.meta['proxy'] = "http://" + ip + ':' + PROXY_PORT[ip]
        print "####request with proxy: {}###".format(request.meta['proxy'])
        # Use the following lines if your proxy requires authentication
        #  proxy_user_pass = "USERNAME:PASSWORD"
        # setup basic authentication for the proxy
        #  proxy_user_pass = ""
        #  encoded_user_pass = base64.encodestring(proxy_user_pass)
        #  request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
