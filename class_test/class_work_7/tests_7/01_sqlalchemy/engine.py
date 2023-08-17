from faker import Faker
from sqlalchemy.sql import select
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    MetaData,
    create_engine,
)


fake = Faker()

engine = create_engine("sqlite:///test_hw_7.db")
metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("fullname", String),
)

adresses = Table(
    "adress",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("email_adress", String, nullable=False),
)

metadata.create_all(engine)

with engine.connect() as conn:
    ins = users.insert().values(name=f"{fake.name()}", fullname=f"{fake.name()}")
    result = conn.execute(ins)

    s = select(users)
    result = conn.execute(s)

    for row in result:
        print(row)
