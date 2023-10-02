import unittest
from unittest.mock import MagicMock

from sqlalchemy import and_
from sqlalchemy.orm import Session
from src.database.models import User
from src.schemas import ContactsModel, ResponseContacts
from datetime import date, timedelta
from src.repository.contacts import (
    create_contact,
    read_contacts,
    get_contact,
    update_contact,
    remove_contact,
    search_contacts,
    serch_by_birthday,
)


class TestContacts(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_create_contact(self):
        user = User(username="testuser", password="testpassword")
        self.session.add(user)
        self.session.commit()

        contact_data = ResponseContacts(
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            phone_number="1234567890",
            birthday_date=date(1990, 1, 1),
        )

        contact = create_contact(contact_data, user, self.session)

        self.assertEqual(contact.first_name, "John")
        self.assertEqual(contact.last_name, "Doe")
        self.assertEqual(contact.email, "johndoe@example.com")

    async def test_read_contacts(self):
        user = User(username="testuser", password="testpassword")
        self.session.add(user)
        self.session.commit()

        for i in range(5):
            contact_data = ResponseContacts(
                first_name=f"Contact{i}",
                last_name=f"Lastname{i}",
                email=f"contact{i}@example.com",
                phone_number="1234567890",
                birthday_date=date(1990, 1, 1),
            )
            create_contact(contact_data, user, self.session)

        contacts = read_contacts(0, 10, user, self.session)
        self.assertEqual(len(contacts), 5)

    async def test_get_contact(self):
        user = User(username="testuser", password="testpassword")
        self.session.add(user)
        self.session.commit()

        contact_data = ResponseContacts(
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            phone_number="1234567890",
            birthday_date=date(1990, 1, 1),
        )
        created_contact = create_contact(contact_data, user, self.session)

        retrieved_contact = get_contact(created_contact.id, user, self.session)
        self.assertEqual(retrieved_contact.first_name, "John")
        self.assertEqual(retrieved_contact.last_name, "Doe")
        self.assertEqual(retrieved_contact.email, "johndoe@example.com")

    async def test_update_contact(self):
        user = User(username="testuser", password="testpassword")
        self.session.add(user)
        self.session.commit()

        contact_data = ResponseContacts(
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            phone_number="1234567890",
            birthday_date=date(1990, 1, 1),
        )
        created_contact = create_contact(contact_data, user, self.session)

        updated_data = ContactsModel(
            first_name="UpdatedJohn",
            last_name="UpdatedDoe",
            email="updatedjohndoe@example.com",
            phone_number="9876543210",
            birthday_date=date(1995, 5, 5),
        )

        updated_contact = update_contact(
            created_contact.id, updated_data, user, self.session
        )

        self.assertEqual(updated_contact.first_name, "UpdatedJohn")
        self.assertEqual(updated_contact.last_name, "UpdatedDoe")
        self.assertEqual(updated_contact.email, "updatedjohndoe@example.com")
        self.assertEqual(updated_contact.phone_number, "9876543210")

    async def test_remove_contact(self):
        user = User(username="testuser", password="testpassword")
        self.session.add(user)
        self.session.commit()

        contact_data = ResponseContacts(
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            phone_number="1234567890",
            birthday_date=date(1990, 1, 1),
        )
        created_contact = create_contact(contact_data, user, self.session)

        removed_contact = remove_contact(created_contact.id, user, self.session)
        self.assertEqual(removed_contact.id, created_contact.id)
        self.assertIsNone(get_contact(created_contact.id, user, self.session))

    async def test_search_contacts(self):
        user = User(username="testuser", password="testpassword")
        self.session.add(user)
        self.session.commit()

        contact_data = ResponseContacts(
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            phone_number="1234567890",
            birthday_date=date(1990, 1, 1),
        )
        create_contact(contact_data, user, self.session)

        search_result = search_contacts("John", user, self.session)
        self.assertEqual(len(search_result), 1)
        self.assertEqual(search_result[0].first_name, "John")

    async def test_search_by_birthday(self):
        user = User(username="testuser", password="testpassword")
        self.session.add(user)
        self.session.commit()

        contact_data = ResponseContacts(
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            phone_number="1234567890",
            birthday_date=date.today() + timedelta(days=5),
        )
        create_contact(contact_data, user, self.session)

        search_result = serch_by_birthday(user, self.session)
        self.assertEqual(len(search_result), 1)
        self.assertEqual(
            search_result[0].birthday_date, date.today() + timedelta(days=5)
        )


if __name__ == "__main__":
    unittest.main()
