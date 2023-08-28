from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from db import username, password, domain, port, db_name
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

url = f"postgresql://{username}:{password}@{domain}:{port}/{db_name}"

engine = create_engine(url, echo=False)
DBSession = sessionmaker(bind=engine)
Base = declarative_base()
Base.metadata.bind = engine


class Quotes(Base):
    __tablename__ = 'quotes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    keywords = Column(String(50))
    author = Column(String(10))
    quote = Column(String(250))


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(30))
    date_born = Column(String(30))
    location_born = Column(String(30))
    bio = Column(String(500))


session = DBSession()