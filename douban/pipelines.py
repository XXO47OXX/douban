# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import openpyxl
import pymysql
class DbPipeline:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost',port=3306,user='root',password='oxx1234560..',database='spider',charset='utf8mb4')
        self.cursor=self.conn.cursor()
        self.data=[]


    def close_spider(self,spider):
        if len(self.data)>0:
            self._writer_to_db()
        #self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        title=item.get('title','')
        rank=item.get('rank',0)
        subject=item.get('subject','')
        self.data.append((title,rank,subject))
        if len(self.data)== 100:
            self._writer_to_db ()
        #self.cursor.execute('insert into tb_top_movie(title,rating,subject) values(%s,%s,%s)',
        #(title,rank,subject))
        return item

    def _writer_to_db(self) :
        self.cursor.executemany (
            'insert into tb_top_movie(title,rating,subject,duration,intro) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)' ,
            self.data
        )
        self.conn.commit ()
        self.data.clear ()


class ExcelPipeline:
    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws =self.wb.active
        self.ws.title='Top250'
        self.ws.append(('标题','评分','主题','时长','简介'))
    def close_spider(self,spider):
        self.wb.save('电影数据.xlsx')

    def process_item(self, item, spider):
        title=item.get('title','')
        rank=item.get('rank','')
        subject=item.get('subject','')
        duration=item.get('duration','')
        intro=item.get('intro','')
        self.ws.append((title,rank,subject,duration,intro))
        return item
