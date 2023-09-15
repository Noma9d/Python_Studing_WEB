from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from src.database.db import engine
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.schema import ForeignKey

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
    user_id = Column(
        "user_id", ForeignKey("users.id", ondelete="CASCADE"), default=None
    )
    user = relationship("User", backref="contacts")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(20))
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(30), nullable=False)
    created_at = Column("created_at", DateTime, default=func.now())
    refresh_token = Column(String(255), nullable=False)
