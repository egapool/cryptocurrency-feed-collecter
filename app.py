# coding: utf-8

import feedparser
url = 'https://medium.com/feed/@ShinichiroMatsuo/'
d = feedparser.parse(url)

for item in d['entries']:
    print(item['title'])
    print(item['link'])
    print(item['published'])
    print(item['updated'])
    print(item['content'][0]['value'][0:200])


