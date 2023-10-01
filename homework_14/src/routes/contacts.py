from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from src.schemas import ResponseContacts, ContactsModel

from src.database.db import get_db
from src.repository import contacts as repository_contacts
from typing import List

from src.database.models import User
from src.services.auth import auth_service

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post(
    "/",
    response_model=ResponseContacts,
    dependencies=[Depends(RateLimiter(times=2, seconds=5))],
)
async def create_contacts(
    body: ContactsModel,
    user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Создает новый контакт.

    Args:
        body (ContactsModel): Модель данных для создания контакта.
        user (User): Аутентифицированный пользователь.
        db (Session): Сессия базы данных.

    Returns:
        ResponseContacts: Созданный контакт.

    """

    return await repository_contacts.create_contact(body, user, db)


@router.get(
    "/",
    response_model=List[ResponseContacts],
    dependencies=[Depends(RateLimiter(times=2, seconds=5))],
)
async def read_contacts(
    skip: int = 1,
    limit: int = 5,
    user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Возвращает список контактов для пользователя с учетом пагинации.

    Args:
        skip (int): Количество контактов для пропуска.
        limit (int): Максимальное количество контактов для возврата.
        user (User): Аутентифицированный пользователь.
        db (Session): Сессия базы данных.

    Returns:
        List[ResponseContacts]: Список контактов пользователя.

    """

    return await repository_contacts.read_contacts(skip, limit, user, db)


@router.get(
    "/{contact_id}",
    response_model=ResponseContacts,
    dependencies=[Depends(RateLimiter(times=2, seconds=5))],
)
async def get_contact(
    contact_id: int,
    user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Возвращает контакт по его идентификатору для пользователя.

    Args:
        contact_id (int): Идентификатор контакта.
        user (User): Аутентифицированный пользователь.
        db (Session): Сессия базы данных.

    Returns:
        ResponseContacts: Контакт с указанным идентификатором.

    """

    contact = await repository_contacts.get_contact(contact_id, user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.put(
    "/{contact_id}",
    response_model=ResponseContacts,
    dependencies=[Depends(RateLimiter(times=2, seconds=5))],
)
async def update_contact(
    contact_id: int,
    body: ContactsModel,
    user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Обновляет информацию о контакте для пользователя.

    Args:
        contact_id (int): Идентификатор контакта, который нужно обновить.
        body (ContactsModel): Новые данные контакта.
        user (User): Аутентифицированный пользователь.
        db (Session): Сессия базы данных.

    Returns:
        ResponseContacts: Обновленный контакт.

    """

    contact = await repository_contacts.update_contact(contact_id, body, user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.delete(
    "/{contact_id}",
    response_model=ResponseContacts,
    dependencies=[Depends(RateLimiter(times=2, seconds=5))],
)
async def delete_contact(
    contact_id: int,
    user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Удаляет контакт по его идентификатору для пользователя.

    Args:
        contact_id (int): Идентификатор контакта, который нужно удалить.
        user (User): Аутентифицированный пользователь.
        db (Session): Сессия базы данных.

    Returns:
        ResponseContacts: Удаленный контакт.

    """

    contact = await repository_contacts.remove_contact(contact_id, user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.get(
    "/search_contact",
    response_model=List[ResponseContacts],
    dependencies=[Depends(RateLimiter(times=2, seconds=5))],
)
async def search_contacts(
    query: str = Query(None, title="Search contact by first_name, last_name or email"),
    user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    """
    Выполняет поиск контактов по запросу для пользователя.

    Args:
        query (str): Строка запроса для поиска в имени, фамилии или электронной почте контактов.
        user (User): Аутентифицированный пользователь.
        db (Session): Сессия базы данных.

    Returns:
        List[ResponseContacts]: Список контактов, соответствующих запросу.

    """

    contacts = await repository_contacts.search_contacts(query, user, db)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )

    return contacts


@router.get(
    "/birthday_date",
    response_model=List[ResponseContacts],
    dependencies=[Depends(RateLimiter(times=2, seconds=5))],
)
async def search_by_birthday(
    user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)
):
    """
    Выполняет поиск контактов с днями рождения, находящимися в ближайших 7 днях, для пользователя.

    Args:
        user (User): Аутентифицированный пользователь.
        db (Session): Сессия базы данных.

    Returns:
        List[ResponseContacts]: Список контактов с ближайшими днями рождения.

    """

    contacts = await repository_contacts.serch_by_birthday(user, db)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )

    return contacts
