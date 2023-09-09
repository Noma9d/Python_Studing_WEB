from typing import Optional

from pydantic import BaseModel, Field, EmailStr, HttpUrl


class User(BaseModel):
    name: str
    email: EmailStr
    website: HttpUrl
    age: Optional[int] = Field(None, ge=13, le=90)
    friends: Optional[int] = 0


user = User(name="John", email="john@example.com", website="https://john.com", age=25, friends=10)
print(user)

user = User(name="Jane", email="jane@example.com", website="https://jane.com", age=12)
print(user)

user = User(name="Bob", email="bob@example.com", website="invalid url", age=20)
print(user)