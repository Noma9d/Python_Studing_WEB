from sqlalchemy.orm import Session
from src.database.models import User
from src.schemas import UserModel


async def get_user_from_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session):
    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return new_user


async def update_token(user: User, token: str | None, db: Session):
    user.refresh_token = token
    db.commit()
