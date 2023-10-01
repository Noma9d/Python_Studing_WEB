from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from src.database.db import engine
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.schema import ForeignKey

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Contact(Base):
    """
    Модель для хранения информации о контактах.

    Attributes:
        id (int): Уникальный идентификатор контакта.
        first_name (str): Имя контакта (до 20 символов, обязательное поле, индексируется).
        last_name (str): Фамилия контакта (до 20 символов).
        email (str): Адрес электронной почты контакта (до 20 символов, уникальный, индексируется).
        phone_number (str): Номер телефона контакта (до 20 символов, уникальный, индексируется).
        birthday_date (datetime): Дата рождения контакта (тип TIMESTAMP).
        user_id (int): Идентификатор пользователя, связанного с данным контактом.
        user (User): Связь с моделью пользователя (User).

    """

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
    """
    Модель для хранения информации о пользователях.

    Attributes:
        id (int): Уникальный идентификатор пользователя.
        username (str): Имя пользователя (до 20 символов).
        email (str): Адрес электронной почты пользователя (до 30 символов, обязательное поле, уникальный).
        password (str): Пароль пользователя (до 30 символов, обязательное поле).
        created_at (datetime): Дата создания пользователя (тип DateTime, устанавливается по умолчанию).
        refresh_token (str): Токен обновления пользователя (до 255 символов, обязательное поле).

    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(20))
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(30), nullable=False)
    created_at = Column("created_at", DateTime, default=func.now())
    refresh_token = Column(String(255), nullable=False)
