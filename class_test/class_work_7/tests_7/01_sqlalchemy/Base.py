from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


engine = create_engine("postrgesql://Nom@d:12345@localhost:5432/sruding_db.db")
DBSession = sessionmaker(bind=engine)
# session = DBSession()

Base = declarative_base()


class Person(Base):
    __tablename__ = "person"
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Adress(Base):
    __tablename__ = "adresses"
    id = Column(Integer, primary_key=True)
    street_name = Column(String(250))
    street_number = Column(String(250))
    post_code = Column(String(250), nullable=False)
    person_id = Column(Integer, ForeignKey("person.id"))
    person = relationship(Person)


Base.metadata.create_all(engine)
Base.metadata.bind = engine

with DBSession() as session:
    new_person = Person(name="Smit")
    new_adresses = Adress(post_code="6666", person=new_person, street_number=77)
    session.add(new_person)  # Create
    session.add(new_adresses)
    session.commit()

    user_1 = session.query(Person).get(2)  # Read
    print(user_1.id, user_1.name)

    article = session.query(Person).get(4)  # Delete
    session.delete(article)
    session.commit()
