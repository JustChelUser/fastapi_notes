from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings

settings = get_settings()
engine = create_engine(str(settings.DATABASE_URL))
Session_local = sessionmaker(bind=engine)


def get_db():
    db = Session_local()
    try:
        yield db
    finally:
        db.close()
