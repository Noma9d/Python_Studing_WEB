from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.database.db import engine


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(20), nullable=False, index=True)
    last_name = Column(String(20), nullable=True)
    email = Column(String(20), unique=True, index=True)
    phone_number = Column(String(20), unique=True, index=True)
    birthday_date = Column(TIMESTAMP)
