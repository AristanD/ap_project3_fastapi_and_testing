import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from db.base import Base
from db.session import get_db


TEST_DB = "sqlite:///./test.db"

engine = create_engine(TEST_DB)
TestingSessionLocal = sessionmaker(bind=engine)


# Фикстура базы данных (искусственного окружения для теста)
@pytest.fixture(scope="session")
def db():
    Base.metadata.create_all(bind=engine)   # Создание тестовой БД
    yield
    Base.metadata.drop_all(bind=engine)     # Удаление метаданных после теста


# Фикстура локальной тестовой сессии БД
@pytest.fixture()
def session(db):
    connection = engine.connect()
    transaction = connection.begin()

    db = TestingSessionLocal(bind=connection)
    yield db

    db.close()
    transaction.rollback()  # Автоматический откат БД после теста
    connection.close()


# Фикстура клиента
@pytest.fixture()
def client(session):

    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)