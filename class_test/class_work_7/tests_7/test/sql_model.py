from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# from db import username, password, domain, port, db_name


# url = f'postgresql://{username}:{password}@{domain}:{port}/{db_name}'
url = "sqlite:///:memory:"


engine = create_engine(url, echo=True)
DBSession = sessionmaker(bind=engine)
Base = declarative_base()
Base.metadata.bind = engine


class Groups(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), nullable=False)
    students = relationship("Students", back_populates="group")


class Students(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), nullable=False)
    id_group = Column(
        Integer, ForeignKey("groups.id", ondelete="SET NULL", onupdate="CASCADE")
    )
    group = relationship("Groups", back_populates="students")
    grades = relationship("Grades", back_populates="student")


class Teachers(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), nullable=False)
    items = relationship("Items", back_populates="teacher")


class Items(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), nullable=False)
    id_teacher = Column(
        Integer, ForeignKey("teachers.id", ondelete="SET NULL", onupdate="CASCADE")
    )
    teacher = relationship("Teachers", back_populates="items")
    grades = relationship("Grades", back_populates="items")


class Grades(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_student = Column(
        Integer, ForeignKey("students.id", ondelete="SET NULL", onupdate="CASCADE")
    )
    id_item = Column(
        Integer, ForeignKey("items.id", ondelete="SET NULL", onupdate="CASCADE")
    )
    grade = Column(Integer)
    crated_at = Column(DateTime, default=datetime.now())
    student = relationship("Students", back_populates="grades")
    items = relationship("Items", back_populates="grades")


Base.metadata.create_all(engine)
session = DBSession()
