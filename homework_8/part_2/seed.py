from connect_db import conn
from faker import Faker
from models import Contact


def seed_data(quantity_contact: int) -> None:
    fake = Faker()
    count = 0
    while count < quantity_contact:
        Contact(
            fullname=fake.name(), email=fake.email(), phone_number=fake.phone_number()
        ).save()
        count += 1


if __name__ == "__main__":
    conn
    seed_data(500)
