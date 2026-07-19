from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session
from fastapi import status

from app.core.PasswordManager import PasswordManager
from app.repositories.UserRepository import UserRepository
from app.schemas.User import UserCreateSchema, UserReadSchema


class UserService:

    def __init__(self, db: Session) -> None:
        self.db = db
        self.user_repository = UserRepository(self.db)

    def list_user(self) -> list[UserReadSchema]:
        users = self.user_repository.get_all()
        return [UserReadSchema.model_validate(user) for user in users]

    def register_user(self, user_data: UserCreateSchema) -> UserReadSchema:
        existing_user = self.user_repository.get_by_username(user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким именем уже существует"
            )
        hashed_password = PasswordManager.hash_password(user_data.password)
        try:
            new_user = self.user_repository.create(
                username=user_data.username,
                hashed_password=hashed_password
            )
            return UserReadSchema.model_validate(new_user)
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ошибка регистрации : имя уже занято"
            )

    def get_user_by_username(self, username: str) -> UserReadSchema:
        user = self.user_repository.get_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        return UserReadSchema.model_validate(user)

    def login_user(self, login_data: UserCreateSchema) -> str:
        user = self.user_repository.get_by_username(login_data.username)
        if not user or not PasswordManager.verify_password(login_data.password, str(user.hashed_password)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверное имя пользователя или пароль"
            )
        token_data = {"sub": user.username, "user_id": user.id}
        return PasswordManager.create_access_token(data=token_data)
