from sqlalchemy.orm import Session
from src.database.models import User
from src.schemas import UserModel
from libgravatar import Gravatar


async def get_user_from_email(email: str, db: Session):
    """
    Получает пользователя из базы данных по адресу электронной почты.

    Args:
        email (str): Адрес электронной почты пользователя.
        db (Session): Сессия SQLAlchemy для работы с базой данных.

    Returns:
        User | None: Экземпляр пользователя, если найден, в противном случае None.
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session):
    """
    Создает нового пользователя на основе данных из модели UserModel.

    Args:
        body (UserModel): Модель данных пользователя.
        db (Session): Сессия SQLAlchemy для работы с базой данных.

    Returns:
        User: Новый экземпляр пользователя.
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return new_user


async def update_token(user: User, token: str | None, db: Session):
    """
    Обновляет токен пользователя.

    Args:
        user (User): Экземпляр пользователя, которому нужно обновить токен.
        token (str | None): Новый токен пользователя или None, если токен должен быть удален.
        db (Session): Сессия SQLAlchemy для работы с базой данных.

    Returns:
        None
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    Подтверждает адрес электронной почты пользователя.

    Args:
        email (str): Адрес электронной почты, который нужно подтвердить.
        db (Session): Сессия SQLAlchemy для работы с базой данных.

    Returns:
        None
    """
    user = await get_user_from_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email: str, url: str, db: Session) -> User:
    """
    Обновляет аватар пользователя.

    Args:
        email (str): Адрес электронной почты пользователя, у которого нужно обновить аватар.
        url (str): URL нового аватара пользователя.
        db (Session): Сессия SQLAlchemy для работы с базой данных.

    Returns:
        User: Экземпляр пользователя с обновленным аватаром.
    """
    user = await get_user_from_email(email, db)
    user.avatar = url
    db.commit()
    return user
