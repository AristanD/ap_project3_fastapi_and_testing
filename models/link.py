from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from db.base import Base


class Link(Base):
    """Модель таблицы ссылок"""

    __tablename__ = "links"

    id = Column(Integer, primary_key=True)                      # айди

    orig_url = Column(String, nullable=False)                   # исходная ссылка (длинная)
    short_code = Column(String, unique=True, index=True)        # короткая ссылка (сгенерированная)
    custom_alias = Column(String, unique=True, nullable=True)   # вариант от пользователя

    created_dt = Column(DateTime, server_default=func.now())    # Дата создания
    expires_dt = Column(DateTime, nullable=True)                # Дата истечения срока хранения
    last_accessed_dt = Column(DateTime, nullable=True)          # Последний запрос

    click_cnt = Column(Integer, default=0)                      # Кол-во обращений

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)    # id пользователя, создавшего короткую ссылку

    project = Column(String, nullable=True)                     # Название проекта