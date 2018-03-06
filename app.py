
# coding: utf-8

# In[ ]:


# coding: utf-8
# %load_ext autoreload
# %autoreload 2

import feedparser
import pymysql.cursors

import html_parser
import config
import feeds

print('start')
connection = pymysql.connect(
    host=config.DATABASES['HOST'],
    user=config.DATABASES['USER'],
    passwd=config.DATABASES['PASSWORD'],
    db=config.DATABASES['NAME'],
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

for url in feeds.URLS:
    d = feedparser.parse(url)
    feeds = []
    for item in d['entries']:
        print(item['title'])
        print(item['link'])
        print(item['published'])
        print(item['updated'])
        print(item['content'][0]['value'][0:200])
        body = html_parser.strip_tags(item['content'][0]['value'])[0:200]
        
        with connection.cursor() as cursor:
            sql = "INSERT INTO feeds (`title`,`url`,`body`) VALUES (%s,%s,%s)"
            r = cursor.execute(sql, (item['title'],item['link'],body))
            print(r) # -> 1
            # autocommitではないので、明示的にコミットする
            connection.commit()
            
connection.close()


