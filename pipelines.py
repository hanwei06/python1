# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
from collections import OrderedDict
import happybase
from scrapy.conf import settings
import time
import pymongo


class DzwPipeline(object):

    # def __init__(self):
    #     connection = pymongo.MongoClient(
    #         settings['MONGODB_SERVER'],
    #         settings['MONGODB_PORT']
    #     )
    #     db = connection[settings['MONGODB_DB']]
    #     self.collection = db[settings['MONGODB_COLLECTION']]
    #
    # def process_item(self, item, spider):
    #
    #     count = self.collection.count({"title": item['title'], "time": item['time'], "url": item['url']})  # 判断是否重复
    #     if count == 0:
    #         self.collection.insert(dict(item))
    #         return item
    #     else:
    #         pass

    # def __init__(self):
    #     host = settings['HBASE_HOST']
    #     table_name = settings['HBASE_TABLE']
    #     connection = happybase.Connection(host)
    #     table = connection.table(table_name)
    #     self.table = table
    #
    # def process_item(self, item, spider):
    #     title = item['title']
    #     date = item['time']
    #     url = item['url']
    #     content = item['content']
    #     t = time.time()
    #     t = int(t)
    #     # md5((url + str(t)).encode("UTF-8")).hexdigest()
    #     self.table.put(url,
    #                    {'YQ_INFO:title ': title, 'YQ_INFO:date': date, 'YQ_INFO:content': content, 'YQ_INFO:site': '大众网'})
    #     return item

    def __init__(self):
        self.filename = 'ttttttttt.txt'

    def process_item(self, item, spider):
        file = codecs.open(self.filename, 'a', encoding='utf-8')
        line = json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + "\n"
        file.write(line)
        file.close()
        return item
