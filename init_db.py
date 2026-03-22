from db.session import engine
from db.base import Base

from models.user import User
from models.link import Link


Base.metadata.create_all(bind=engine)

print("Tables created")     # Вариант создания таблицы без использования alembic (не стал заморачиваться)