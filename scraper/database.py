# database.py
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
import time

Base = declarative_base()

tableName = f'scraped_items' 

class ScrapedItem(Base):
    __tablename__ = tableName
    
    id = Column(Integer, primary_key=True)
    question_uid = Column(Text)
    question_text = Column(Text)
    point_value = Column(Integer)
    # answers
    answer_1_text = Column(Text)
    answer_2_text = Column(Text)
    answer_3_text = Column(Text)
    answer_1_value = Column(Boolean)
    answer_2_value = Column(Boolean)
    answer_3_value = Column(Boolean)
    hint_text = Column(Text)
    
    # Add more columns as needed for your specific scraping needs

def init_db():
    
    engine = create_engine(f'{DATABASE_URL}_{time.time()}.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def save_item(session, item_data):
    item = ScrapedItem(**item_data)
    
    session.add(item)
    session.commit()
    return item