# database.py
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

Base = declarative_base()

class ScrapedItem(Base):
    __tablename__ = 'scraped_items'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    description = Column(Text)
    url = Column(String(255))
    # Add more columns as needed for your specific scraping needs

def init_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def save_item(session, item_data):
    item = ScrapedItem(**item_data)
    session.add(item)
    session.commit()
    return item