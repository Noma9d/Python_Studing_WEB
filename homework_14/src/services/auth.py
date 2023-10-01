from typing import Optional

from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.repository import users as repository_users

from src.config.config import settings
from redis import Redis


class Auth:
    """
    Класс, предоставляющий функции аутентификации и управления токенами.

    Attributes:
        pwd_context (CryptContext): Контекст для хеширования паролей.
        SECRET_KEY (str): Секретный ключ для подписи токенов.
        ALGORITHM (str): Алгоритм подписи токенов.
        oauth2_scheme (OAuth2PasswordBearer): Схема аутентификации OAuth2.
    """

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

    def verify_password(self, plain_passwor, hashed_password):
        """
        Проверяет, совпадают ли пароль в открытом виде и его хешированный эквивалент.

        Args:
            plain_password (str): Пароль в открытом виде.
            hashed_password (str): Хешированный пароль.

        Returns:
            bool: True, если пароли совпадают, в противном случае False.
        """

        return self.pwd_context(plain_passwor, hashed_password)

    def get_password_hash(self, password: str):
        """
        Генерирует хеш пароля.

        Args:
            password (str): Пароль в открытом виде.

        Returns:
            str: Хешированный пароль.
        """

        return self.pwd_context.hash(password)

    async def create_access_token(
        self, data: dict, expires_delta: Optional[float] = None
    ):
        """
        Создает токен доступа.

        Args:
            data (dict): Данные, которые будут закодированы в токене.
            expires_delta (Optional[float]): Срок действия токена в секундах.

        Returns:
            str: Токен доступа.
        """

        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=1)
        to_encode.update(
            {"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"}
        )
        encoded_access_token = jwt.encode(
            to_encode, self.SECRE_KEY, algorithm=self.ALGORITHM
        )
        return encoded_access_token

    async def created_refresh_token(
        self, data: dict, expires_delta: Optional[float] = None
    ):
        """
        Создает токен обновления.

        Args:
            data (dict): Данные, которые будут закодированы в токене.
            expires_delta (Optional[float]): Срок действия токена в секундах.

        Returns:
            str: Токен обновления.
        """

        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update(
            {"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"}
        )
        encoded_refresh_token = jwt.encode(
            to_encode, self.SECRE_KEY, algorithm=self.ALGORITHM
        )
        return encoded_refresh_token

    async def decode_refresh_token(self, refresh_token: str):
        """
        Декодирует токен обновления.

        Args:
            refresh_token (str): Токен обновления.

        Returns:
            str: Email пользователя, связанного с токеном.

        Raises:
            HTTPException: Если токен не может быть декодирован или имеет неверный scope.
        """

        try:
            payload = jwt.decode(
                refresh_token, self.SECRE_KEY, algorithms=[self.ALGORITHM]
            )
            if payload["scope"] == "refresh_token":
                email = payload["sub"]
                return email
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid scope for token",
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

    async def get_current_user(
        self, token: str = Depends(oauth2_schemas), db: Session = Depends(get_db)
    ):
        """
        Получает текущего аутентифицированного пользователя на основе токена доступа.

        Args:
            token (str): Токен доступа.
            db (Session): Сессия базы данных.

        Returns:
            User: Модель данных пользователя.

        Raises:
            HTTPException: Если токен не может быть декодирован или аутентифицированный пользователь не найден.
        """

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload["scope"] == "access_token":
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            raise credentials_exception

        user = await repository_users.get_user_by_email(email, db)
        if user is None:
            raise credentials_exception
        return user

    def create_email_token(self, data: dict):
        """
        Создает токен для подтверждения адреса электронной почты.

        Args:
            data (dict): Данные, которые будут закодированы в токене.

        Returns:
            str: Токен для подтверждения адреса электронной почты.
        """

        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token

    async def get_email_from_token(self, token: str):
        """
        Извлекает адрес электронной почты из токена подтверждения адреса электронной почты.

        Args:
            token (str): Токен подтверждения адреса электронной почты.

        Returns:
            str: Адрес электронной почты пользователя, связанного с токеном.

        Raises:
            HTTPException: Если токен не может быть декодирован или является недействительным.
        """

        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email = payload["sub"]
            return email
        except JWTError as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid token for email verification",
            )

    r = Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        password=settings.redis_password,
        db=0,
    )


auth_service = Auth()
