# coding: utf-8
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date
from assets.database_dash import Base
from datetime import datetime as dt

#Table情報
class Data(Base):
    #TableNameの設定
    __tablename__ = "data"
    #Column情報を設定する
    id = Column(Integer, primary_key=True)

    no = Column(String, unique=False)
    talent = Column(String, unique=False)
    url = Column(String, unique=False)
    #date = Column(Date, unique=False)
    magazine = Column(String, unique=False)
    magazine_kana = Column(String, unique=False)
    year = Column(Integer, unique=False)
    month = Column(Integer, unique=False)

    timestamp = Column(DateTime, default=dt.now())


    def __init__(self, no=None, talent=None, url=None, date=None, magazine=None, magazine_kana=None,
    year=None, month=None, timestamp=None):
        self.no = no
        self.talent = talent
        self.url = url
        #self.date = date
        self.magazine = magazine
        self.magazine_kana = magazine_kana
        self.year = year
        self.month = month
        self.timestamp = timestamp
