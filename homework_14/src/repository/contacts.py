from sqlalchemy import and_
from sqlalchemy.orm import Session
from src.database.models import Contact, User
from src.schemas import ContactsModel, ResponseContacts
from datetime import date, timedelta


async def create_contact(body: ResponseContacts, user: User, db: Session):
    """
    Создает новый контакт и сохраняет его в базе данных.

    Args:
        body (ResponseContacts): Данные контакта для создания.
        user (User): Пользователь, который создает контакт.
        db (Session): Сессия базы данных.

    Returns:
        Contact: Созданный контакт.

    """

    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone_number=body.phone_number,
        birthday_date=body.birthday_date,
        user=user,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def read_contacts(skip: int, limit: int, user: User, db: Session):
    """
    Возвращает список контактов для конкретного пользователя с учетом пагинации.

    Args:
        skip (int): Количество контактов, которые нужно пропустить.
        limit (int): Максимальное количество контактов, которые нужно вернуть.
        user (User): Пользователь, для которого нужно получить контакты.
        db (Session): Сессия базы данных.

    Returns:
        List[Contact]: Список контактов пользователя.

    """

    return (
        db.query(Contact)
        .filter(Contact.user_id == user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


async def get_contact(contact_id: int, user: User, db: Session):
    """
    Возвращает контакт по его идентификатору для конкретного пользователя.

    Args:
        contact_id (int): Идентификатор контакта.
        user (User): Пользователь, для которого нужно получить контакт.
        db (Session): Сессия базы данных.

    Returns:
        Contact: Контакт с указанным идентификатором, принадлежащий пользователю.

    """

    return (
        db.query(Contact)
        .filter(and_(Contact.id == contact_id, Contact.user_id == user.id))
        .first()
    )


async def update_contact(contact_id: int, body: ContactsModel, user: User, db: Session):
    """
    Обновляет информацию о контакте для конкретного пользователя.

    Args:
        contact_id (int): Идентификатор контакта, который нужно обновить.
        body (ContactsModel): Новые данные контакта.
        user (User): Пользователь, для которого нужно обновить контакт.
        db (Session): Сессия базы данных.

    Returns:
        Contact: Обновленный контакт.

    """

    contact = (
        db.query(Contact)
        .filter(and_(Contact.id == contact_id, Contact.user_id == user.id))
        .first()
    )
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday_date = body.birthday_date
        db.commit()

    return contact


async def remove_contact(contact_id: int, user: User, db: Session):
    """
    Удаляет контакт по его идентификатору для конкретного пользователя.

    Args:
        contact_id (int): Идентификатор контакта, который нужно удалить.
        user (User): Пользователь, для которого нужно удалить контакт.
        db (Session): Сессия базы данных.

    Returns:
        Contact: Удаленный контакт.

    """

    contact = (
        db.query(Contact)
        .filter(and_(Contact.id == contact_id, Contact.user_id == user.id))
        .first()
    )
    if contact:
        db.delete(contact)
        db.commit()

    return contact


async def search_contacts(query: str, user: User, db: Session):
    """
    Выполняет поиск контактов по запросу, с учетом конкретного пользователя.

    Args:
        query (str): Строка запроса для поиска в имени, фамилии и электронной почте контактов.
        user (User): Пользователь, для которого выполняется поиск контактов.
        db (Session): Сессия базы данных.

    Returns:
        List[Contact]: Список контактов, соответствующих запросу.

    """

    result = []
    contcts_db = db.query(Contact).filter(Contact.user_id == user.id).all()
    if query:
        for contact in contcts_db:
            if (
                query.lower() in contact["first_name"].lower()
                or query.lower() in contact["last_name"].lower()
                or query.lower() in contact["email"].lower()
            ):
                result.append(Contact(**contact))

    return result


async def serch_by_birthday(user: User, db: Session):
    """
    Выполняет поиск контактов с днями рождения, находящимися в ближайших 7 днях.

    Args:
        user (User): Пользователь, для которого выполняется поиск контактов.
        db (Session): Сессия базы данных.

    Returns:
        List[Contact]: Список контактов с ближайшими днями рождения.

    """

    result = []
    today = date.today()
    end_day = today + timedelta(days=7)

    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()

    for contact in contacts:
        birthda_date = contact["birthday_date"]
        if birthda_date and today <= birthda_date <= end_day:
            result.append(Contact(**contact))

    return result
