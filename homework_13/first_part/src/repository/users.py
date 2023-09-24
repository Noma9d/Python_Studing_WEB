from sqlalchemy.orm import Session
from src.database.models import User
from src.schemas import UserModel
from libgravatar import Gravatar


async def get_user_from_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session):
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
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    user = await get_user_from_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email: str, url: str, db: Session) -> User:
    user = await get_user_from_email(email, db)
    user.avatar = url
    db.commit()
    return user
