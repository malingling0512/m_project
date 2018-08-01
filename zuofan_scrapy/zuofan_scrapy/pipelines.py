# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.pipelines.images import ImagesPipeline

class ZuofanScrapyPipeline(object):
    def process_item(self, item, spider):
        return item

#存储json文件---自定义
class MyjsonPileline():
    def process_item(self, item, spider):   #函数名固定
        print("item:", item)

        with open('item.json','w',encoding='utf-8')as f:
            json.dump(dict(item),f,ensure_ascii=False)

#图片名字处理
class ZuofanImage(ImagesPipeline):
    def item_completed(self, results, item, info):
        imgpath = results[0][1]['path']
        item['titleimage'] = imgpath
        return item

#利用异步框架twisted实现数据库操作
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi   #异步数据库操作函数

class TwistedMysql():
    def __init__(self,mypool):
        self.mypool=mypool

    @classmethod
    def from_settings(cls, settings):     #cls--表示当前类
        dbarg = dict(
            host=settings['MYSQLHOST'],
            user=settings['MYSQLUSER'],
            password=settings['MYSQLPASSWORD'],
            db=settings['MYSQLDB'],
            charset="utf8",
            use_unicode=True,
            cursorclass=MySQLdb.cursors.DictCursor
        )

        # 异步连接池,'MySQLdb'---固定
        db_pool = adbapi.ConnectionPool('MySQLdb', **dbarg)
        return cls(db_pool)

    def process_item(self, item, spider):
        # 调用twisted框架，将数据库插入变成异步（执行数据操作函数，item）
        self.mypool.runInteraction(self.dbinsert, item)

    def dbinsert(self, cursor, item):
        sql = "insert into zuofanspider(title,time_new,cook,source,look_num,abstract,str_yl,str_tl,str_jq,str_bz,imgpath) values('" + item['title'] + "','" + item['time_new'] + ",','" + item['cook'] + "','" + item['source'] + "','" + item['look_num'] + "','" + item['abstract'] + "','" + item['str_yl'] + "','" + item['str_tl'] + "','" + item['str_jq'] + "','" + item['str_bz'] + "','" + item['titleimage'] + "') "
        cursor.execute(sql)