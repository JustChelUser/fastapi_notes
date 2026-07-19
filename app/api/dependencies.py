import jwt
from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_db
from app.models import User
from app.repositories.NoteRepository import NoteRepository
from app.repositories.UserRepository import UserRepository
from app.services.NoteService import NoteService
from app.services.UserService import UserService

settings = get_settings()



def get_user_repo(db: Session = Depends(get_db))->UserRepository:
    return UserRepository(db)
def get_note_repo(db: Session = Depends(get_db))->NoteRepository:
    return NoteRepository(db)

def get_user_service(db: Session = Depends(get_db))->UserService:
    return UserService(db)
def get_note_service(db: Session = Depends(get_db))->NoteService:
    return NoteService(db)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        user_repo: UserRepository = Depends(get_user_repo),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось валидировать учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = user_repo.get_by_username(username)
    if user is None:
        raise credentials_exception
    return user
