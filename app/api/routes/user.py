from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import get_user_service
from app.schemas.User import UserReadSchema, UserCreateSchema
from app.services.UserService import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def list_users(service: UserService = Depends(get_user_service)):
    return service.list_user()


@router.post("/register", response_model=UserReadSchema, status_code=status.HTTP_201_CREATED)
def register(
        user_data: UserCreateSchema,
        service: UserService = Depends(get_user_service)):
    return service.register_user(user_data)


@router.post("/login")
def login(
        login_data: OAuth2PasswordRequestForm = Depends(),
        service: UserService = Depends(get_user_service)):
    token = service.login_user(login_data)
    return {"access_token": token, "token_type": "bearer"}

