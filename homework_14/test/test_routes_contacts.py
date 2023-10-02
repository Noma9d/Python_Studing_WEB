from test.conftest import session
from fastapi.testclient import TestClient
from homework_14.main import app
from homework_14.src.database.models import User, Contact
from datetime import datetime, timedelta
import json

client = TestClient(app)


def test_create_user(session):
    user = User(
        username="testuser", email="Woodpeker@example.com", password="testpassword"
    )

    contact_data = {
        "name": "Woody Woodpeker",
        "email": "woody@example.com",
        "user_id": user.id,
    }

    response = client.post("/", json=contact_data)
    assert response.status_code == 200
    contact = response.json()
    assert contact["name"] == "Woody Woodpeker"
    assert contact["email"] == "woody@example.com"


def test_read_contacts(session):
    user = User(
        username="testuser", email="Woodpeker@example.com", password="testpassword"
    )
    session.add(user)
    session.commit()

    # Вставка тестовых контактов в тестовую базу данных
    contacts = [
        Contact(
            name="Woody Woodpeker 1", email="Woodpeker@example.com", user_id=user.id
        ),
        Contact(
            name="Woody Woodpeker 2", email="Woodpeker@example.com", user_id=user.id
        ),
        # Другие контакты
    ]
    session.add_all(contacts)
    session.commit()

    response = client.get("/")

    assert response.status_code == 200
    contacts = response.json()
    assert isinstance(contacts, list)


def test_get_contact(session):
    user = User(
        username="testuser", email="Woodpeker@example.com", password="testpassword"
    )
    session.add(user)
    session.commit()

    # Вставка тестового контакта в тестовую базу данных
    contact = Contact(
        name="Woody Woodpeker 1", email="Woodpeker@example.com", user_id=user.id
    )
    session.add(contact)
    session.commit()
    response = client.get(f"/{contact.id}")
    assert response.status_code == 200
    contact = response.json()
    assert "name" in contact
    assert "email" in contact


def test_update_contact(session):
    user = User(
        username="testuser", email="Woodpeker@example.com", password="testpassword"
    )
    session.add(user)
    session.commit()

    contact = Contact(
        name="Woody Woodpeker 1", email="Woodpeker@example.com", user_id=user.id
    )
    session.add(contact)
    session.commit()

    update_contact_data = {"name": "John Doe", "email": "john@example.com"}

    response = client.put(f"/{contact.id}", json=update_contact_data)
    assert response.status_code == 200
    update_contact = response.json()
    assert update_contact["name"] == update_contact_data["name"]
    assert update_contact["email"] == update_contact_data["email"]


def test_delete_contact(session):
    user = User(
        username="testuser", email="Woodpeker@example.com", password="testpassword"
    )
    session.add(user)
    session.commit()

    contact = Contact(
        name="Woody Woodpeker 1", email="Woodpeker@example.com", user_id=user.id
    )
    session.add(contact)
    session.commit()

    response = client.delete(f"/{contact.id}")
    assert response.status_code == 200
    delete_contact = response.json()
    assert delete_contact["name"] == contact["name"]
    assert delete_contact["email"] == contact["email"]


def test_search_contacts(session):
    user = User(
        username="Woody", email="Woodpeker@example.com", password="testpassword"
    )
    session.add(user)
    session.commit()

    # Вставка тестовых контактов в тестовую базу данных
    contact1 = Contact(
        name="Woody Woodpeker 1", email="Woodpeker@example.com", user_id=user.id
    )
    contact2 = Contact(
        name="Woody Woodpeker", email="Woodpeker@example.com", user_id=user.id
    )
    contact3 = Contact(
        name="Woody Woodpeker", email="Woodpeker@example.com", user_id=user.id
    )
    session.add_all([contact1, contact2, contact3])
    session.commit()

    response = client.get("/search_contact?query=Woodpeker")
    assert response.status_code == 200
    contacts = response.json()
    assert (
        contacts[0]["name"] == "Woody Woodpeker"
        or contacts[1]["name"] == "Woody Woodpeker"
    )
    assert (
        contacts[0]["name"] == "Woody Woodpeker"
        or contacts[1]["name"] == "Woody Woodpeker"
    )


def test_search_by_birthday(session):
    user = User(username="Woody", email="Woody@example.com", password="testpassword")
    session.add(user)
    session.commit()

    # Создание контакта с днем рождения через 5 дней
    birthday_contact = Contact(
        name="Woody Woodpeker",
        email="Woodpeker@example.com",
        user_id=user.id,
        date_of_birth=datetime.now() + timedelta(days=5),
    )

    session.add(birthday_contact)
    session.commit()

    response = client.get("/birthday_date")

    assert response.status_code == 200
    contacts = response.json()
    assert (
        len(contacts) == 1
    )  # Проверяем, что возвращен только 1 контакт с ближайшим днем рождения
    assert contacts[0]["name"] == "Woody Woodpeker"
