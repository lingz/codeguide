#!/usr/bin/python3.2

import urllib.request

response = urllib.request.urlopen('http://google.com')
html = response.read()

print(html)

