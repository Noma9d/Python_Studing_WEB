from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from src.schemas import ResponseContacts, ContactsModel

from src.database.db import get_db
from src.repository import contacts as repository_contacts
from typing import List

from src.database.models import User
from src.services.auth import auth_service

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=ResponseContacts)
async def create_contacts(
    body: ContactsModel,
    user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    return await repository_contacts.create_contact(body, user, db)


@router.get("/", response_model=List[ResponseContacts])
async def read_contacts(
    skip: int = 1,
    limit: int = 5,
    user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    return await repository_contacts.read_contacts(skip, limit, user, db)


@router.get("/{contact_id}", response_model=ResponseContacts)
async def get_contact(
    contact_id: int,
    user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    contact = await repository_contacts.get_contact(contact_id, user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.put("/{contact_id}", response_model=ResponseContacts)
async def update_contact(
    contact_id: int,
    body: ContactsModel,
    user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    contact = await repository_contacts.update_contact(contact_id, body, user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.delete("/{contact_id}", response_model=ResponseContacts)
async def delete_contact(
    contact_id: int,
    user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    contact = await repository_contacts.remove_contact(contact_id, user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.get("/search_contact", response_model=List[ResponseContacts])
async def search_contacts(
    query: str = Query(None, title="Search contact by first_name, last_name or email"),
    user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    contacts = await repository_contacts.search_contacts(query, user, db)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )

    return contacts


@router.get("/birthday_date", response_model=List[ResponseContacts])
async def search_by_birthday(
    user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)
):
    contacts = await repository_contacts.serch_by_birthday(user, db)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )

    return contacts
