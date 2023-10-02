import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session
from homework_14.src.database.models import User
from homework_14.src.schemas import UserModel
from libgravatar import Gravatar

from homework_14.src.repository.users import (
    create_user,
    get_user_from_email,
    update_avatar,
    update_token,
    confirmed_email,
)
from homework_14.test.conftest import session


class TestUser(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Создаем временную базу данных SQLite для тестов
        self.session = session

    async def test_create_user(self):
        user_data = UserModel(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
        )

        new_user = create_user(user_data, self.session)

        self.assertEqual(new_user.username, "testuser")
        self.assertEqual(new_user.email, "testuser@example.com")

    async def test_get_user_from_email(self):
        user_data = UserModel(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
        )

        create_user(user_data, self.session)

        retrieved_user = get_user_from_email("testuser@example.com", self.session)
        self.assertEqual(retrieved_user.username, "testuser")
        self.assertEqual(retrieved_user.email, "testuser@example.com")

    async def test_update_token(self):
        user_data = UserModel(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
        )

        new_user = create_user(user_data, self.session)
        update_token(new_user, "newtoken", self.session)

        self.assertEqual(new_user.refresh_token, "newtoken")

    async def test_confirmed_email(self):
        user_data = UserModel(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
        )

        new_user = create_user(user_data, self.session)
        confirmed_email(new_user.email, self.session)

        self.assertTrue(new_user.confirmed)

    async def test_update_avatar(self):
        user_data = UserModel(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
        )

        new_user = create_user(user_data, self.session)
        updated_user = update_avatar(new_user.email, "new_avatar_url", self.session)

        self.assertEqual(updated_user.avatar, "new_avatar_url")


if __name__ == "__main__":
    unittest.main()
