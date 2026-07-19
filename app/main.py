from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect

from app.models import Base, User, Note
from app.core.config import get_settings
from app.db.session import engine
from app.api.routes.user import router as user_router
from app.api.routes.note import router as note_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


settings = get_settings()
app = FastAPI(lifespan=lifespan)

app.include_router(router=user_router)
app.include_router(router=note_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_methods=["*"]
)
