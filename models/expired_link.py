from sqlalchemy import Column, Integer, String, DateTime
from db.base import Base


class ExpiredLink(Base):
    """Модель таблицы с историей истёкших ссылок"""

    __tablename__ = "expired_links"

    id = Column(Integer, primary_key=True)
    orig_url = Column(String)
    short_code = Column(String)
    expired_dt = Column(DateTime)