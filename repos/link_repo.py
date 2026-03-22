from sqlalchemy.orm import Session
from models.link import Link


class LinkRepo:
    """Репозиторий ссылок для работы с БД"""

    def __init__(self, db: Session):
        self.db = db


    def create(self, link: Link):
        """Создание ссылки"""

        self.db.add(link)
        self.db.commit()
        self.db.refresh(link)

        return link


    def get_by_code(self, short_code: str):
        """Обращение через короткую ссылку в качестве ключа"""
        return self.db.query(Link).filter(Link.short_code == short_code).first()


    def get_by_original(self, orig_url: str):
        """Обращение через исходную ссылку в качестве ключа"""
        return self.db.query(Link).filter(Link.orig_url == orig_url).first()
    

    def get_by_project(self, project: str):
        """Получение ссылок по названию проекта"""
        return self.db.query(Link).filter(Link.project == project).all()


    def delete(self, link: Link):
        """Удаление инфо о ссылке"""

        self.db.delete(link)
        self.db.commit()


    def update(self, short_code: str, new_url: str):
        """Замена оригинальной ссылки"""
        link = self.get_by_code(short_code)
        if not link:
            return None
        
        link.orig_url = new_url
        
        self.db.commit()
        self.db.refresh(link)

        return link