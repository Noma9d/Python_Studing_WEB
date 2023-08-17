from mongoengine import Document
from mongoengine.fields import (
    StringField,
    BooleanField,
)


class Contact(Document):
    fullname = StringField()
    email = StringField()
    phone_number = StringField()
    send_status = BooleanField(default=False)
