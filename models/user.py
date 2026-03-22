from sqlalchemy import Column, Integer, String
from db.base import Base


class User(Base):
    """Модель пользовательской таблицы"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)  # айдишник
    email = Column(String, unique=True)     # email пользователя
    password_hash = Column(String)          # хэш пароля (напрямую не храню, опасно)