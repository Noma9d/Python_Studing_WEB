from sqlalchemy.orm import Session
from src.database.models import Contact
from src.schemas import ContactsModel, ResponseContacts
from datetime import date, timedelta


async def create_contact(body: ResponseContacts, db: Session):
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone_number=body.phone_number,
        birthday_date=body.birthday_date,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def read_contacts(skip: int, limit: int, db: Session):
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session):
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def update_contact(contact_id: int, body: ContactsModel, db: Session):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday_date = body.birthday_date
        db.commit()

    return contact


async def remove_contact(contact_id: int, db: Session):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()

    return contact


async def search_contacts(query: str, db: Session):
    result = []
    contcts_db = db.query(Contact).all()
    if query:
        for contact in contcts_db:
            if (
                query.lower() in contact["first_name"].lower()
                or query.lower() in contact["last_name"].lower()
                or query.lower() in contact["email"].lower()
            ):
                result.append(Contact(**contact))

    return result


async def serch_by_birthday(db:Session):
    result = []
    today = date.today()
    end_day = today + timedelta(days=7)

    contacts = db.query(Contact).all()

    for contact in contacts:
        birthda_date = contact['birthday_date']
        if birthda_date and today <= birthda_date <= end_day:
            result.append(Contact(**contact))

    return result