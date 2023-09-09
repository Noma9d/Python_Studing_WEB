from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from src.schemas import ResponseContacts, ContactsModel

from src.database.db import get_db
from src.repository import contacts as repository_contacts
from typing import List

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=ResponseContacts)
async def create_contacts(body: ContactsModel, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, db)


@router.get("/", response_model=List[ResponseContacts])
async def read_contacts(skip: int = 1, limit: int = 5, db: Session = Depends(get_db)):
    return await repository_contacts.read_contacts(skip, limit, db)


@router.get("/{contact_id}", response_model=ResponseContacts)
async def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.put("/{contact_id}", response_model=ResponseContacts)
async def update_contact(
    contact_id: int, body: ContactsModel, db: Session = Depends(get_db)
):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.delete("/{contact_id}", response_model=ResponseContacts)
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.get("/search_contact", response_model=List[ResponseContacts])
async def search_contacts(
    query: str = Query(None, title="Search contact by first_name, last_name or email"),
    db: Session = Depends(get_db),
):
    contacts = await repository_contacts.search_contacts(query, db)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )

    return contacts


@router.get('/birthday_date', response_model=List[ResponseContacts])
async def search_by_birthday(db:Session = Depends(get_db)):
    contacts = await repository_contacts.serch_by_birthday(db)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )

    return contacts