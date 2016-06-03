# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

class AppspiderPipeline(object):
    #def open_spider(self, spider):
    def __init__(self):
        self.file = codecs.open('results.json','w',encoding='utf-8')

    def process_item(self, item, spider):
        out = item
        out['tags'] = ','.join(item['tags'])
        line = json.dumps(dict(out),ensure_ascii=False)+'\n'
        self.file.write(line)
        return item

    '''
    def close_spider(self, spider):
        self.file.close()
    '''
