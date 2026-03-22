from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings


engine = create_engine(settings.DB_URL)


# Локальная сессия
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


def get_db():   # Обращение к БД
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()