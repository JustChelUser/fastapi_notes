from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[User]:
        return list(self.db.scalars(select(User)).all())

    def get_by_username(self, username: str) -> User | None:
        statement = select(User).where(User.username == username)
        return self.db.execute(statement).scalar_one_or_none()

    def create(self, username: str, hashed_password: str) -> User:
        user = User(username=username, hashed_password=hashed_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()
