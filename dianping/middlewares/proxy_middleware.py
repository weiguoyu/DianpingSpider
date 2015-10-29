#!/usr/bin/env python
# encoding: utf-8

# Importing base64 library because we'll need it ONLY in case if the proxy we are going to use requires authentication
import base64

YOUR_PROXY_IP = "121.32.52.10"
PORT = "9999"
# Start your middleware class
class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        request.meta['proxy'] = "http://" + YOUR_PROXY_IP + ':' + PORT
        # Use the following lines if your proxy requires authentication
        #  proxy_user_pass = "USERNAME:PASSWORD"
        # setup basic authentication for the proxy
        #  proxy_user_pass = ""
        #  encoded_user_pass = base64.encodestring(proxy_user_pass)
        #  request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
