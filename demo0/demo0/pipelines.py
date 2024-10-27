# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import openpyxl

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .items import db_url,db, DatabaseItem

class DatabasePipeline:
    def __init__(self):
        self.engine = create_engine(db_url)
        db.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def process_item(self, item, spider):
        session = self.Session()
        db_item = DatabaseItem(
            title=item['title'], 
            rank=item['rank'],
            subject=item['subject']
            )
        try:
            session.add(db_item)
            session.commit()
        except Exception as e:
            session.rollback()
            session.flush()
            print(f"Error extracting {e}")

        session.close()

        return item

class MoviePipeline:

    def __init__(self) -> None:
        self.wb = openpyxl.Workbook()    # workbook
        self.ws = self.wb.active      # worksheet
        self.ws.title = 'Top250'
        self.ws.append(('Title','Rank','Subject','duration','intro'))

    def process_item(self, item, spider):
        title = item.get('title','')
        rank = item.get('rank','')
        subject = item.get('subject','')
        duration = item.get('duration','')
        intro = item.get('intro','')

        self.ws.append((title,rank,subject,duration,intro))

        return item
    
    def open_spider(self,spider):
        pass

    def close_spider(self,spider):
        self.wb.save('Movie_data.xlsx')

