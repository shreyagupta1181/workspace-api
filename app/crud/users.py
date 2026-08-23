from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import User
from app.schemas.users import UserCreate, UserUpdate

def create_user(
    db: Session,
    user: UserCreate,
    hashed_password: str,
) -> User:
    db_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_user(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[User]:
    statement = select(User).offset(skip).limit(limit)

    return list(db.scalars(statement).all())

def update_user(
    db: Session,
    user: User,
    user_data: UserUpdate,
    hashed_password: str | None = None,
) -> User:
    update_data = user_data.model_dump(exclude_unset=True)

    if hashed_password is not None:
        update_data["password"] = hashed_password

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()

def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    statement = select(User).where(User.email == email)

    return db.scalars(statement).first()