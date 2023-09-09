from pydantic import BaseModel, EmailStr
from datetime import date


class ContactsModel(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday_date: date


class ResponseContacts(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday_date: date

    class Config:
        orm_mode = True
