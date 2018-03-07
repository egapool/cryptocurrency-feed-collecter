
# coding: utf-8

# In[ ]:


# coding: utf-8
# %load_ext autoreload
# %autoreload 2

import feedparser
import pymysql.cursors
from datetime import datetime

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

try:
    for i in feeds.URLS:
        print(i)
        d = feedparser.parse(i['url'])
        feeds = []
        for item in d['entries']:
            print(item['title'])
            print(item['link'])
            published = datetime.strptime(item['published'],i['tfmt']).strftime('%Y-%m-%d %H:%M:%S')
            print(published)
            print(item['updated'])
    #         print(item['content'][0]['value'][0:200])
            body = html_parser.strip_tags(item['content'][0]['value'])[0:200]

            with connection.cursor() as cursor:
                sql = "INSERT INTO feeds (`title`,`url`,`body`,`published`) VALUES (%s,%s,%s,%s)"
                r = cursor.execute(sql, (item['title'],item['link'],body,published))
    connection.commit()
except Exception as e:
    connection.close()
    print(e)
else:
    connection.close()


