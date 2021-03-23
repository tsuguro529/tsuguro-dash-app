# coding: utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import datetime
import os

import pandas as pd

databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data.db')
engine = create_engine(os.environ.get('DATABASE_URL') or 'sqlite:///' + databese_file, convert_unicode=True , echo=True)
db_session = scoped_session(
                sessionmaker(
                    autocommit = False,
                    autoflush = False,
                    bind = engine
                )
             )
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import assets.models_dash
    Base.metadata.create_all(bind=engine)

def read_data():
    from assets import models_dash
    df = pd.read_csv('assets/analyze_magazine_cover.csv')

    for index, _df in df.iterrows():

        #date = datetime.datetime.strptime(_df['発売日'],'%Y年%m月%d日').date()
        #row = models_dash.Data(no=_df['巻号'], talent=_df['モデル'], url=_df['URL'], date=date, magazine=_df['雑誌名'], magazine_kana=_df['ザッシ名'], year=_df['年'], month=_df['月'])
        row = models_dash.Data(no=_df['no'], talent=_df['talent'], url=_df['url'], magazine=_df['magazine'], magazine_kana=_df['magazine_kana'], year=_df['year'], month=_df['month'])
        db_session.add(row)

    db_session.commit()

KeyError: '巻号'
