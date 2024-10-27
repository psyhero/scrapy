# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from sqlalchemy import Column,Integer,String,Float
from sqlalchemy.ext.declarative import declarative_base


class MovieItem(scrapy.Item):
    title = scrapy.Field()
    rank = scrapy.Field()
    subject = scrapy.Field()
    duration = scrapy.Field()
    intro = scrapy.Field()


db_url = 'mysql+pymysql://root:mm546896@localhost:3306/douban'
db = declarative_base()

class DatabaseItem(db):
    __tablename__ = 'movie_top250'
    id = Column(Integer,primary_key=True,autoincrement=True)
    title = Column(String(55),unique=True,nullable=False)
    rank = Column(Float,default=0)
    subject = Column(String(255),default='')