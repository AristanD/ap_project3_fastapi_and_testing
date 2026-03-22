from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

from models.link import Link
from cache.redis_cache import cache     # экземпляр класса
from utils.link_generator import random_link_generator


class LinkService:
    """Основной сервис по работе с ссылками"""

    def __init__(self, repo):
        self.repo = repo


    def create_link(
        self,
        orig_url,
        custom_alias=None,
        expires_dt=None,
        user_id=None,
        project=None
    ):
        """Непосредственно создание ссылки"""

        if custom_alias:    # Если есть вариант юзера
            
            if self.repo.get_by_code(custom_alias):
                raise Exception("Alias already exists")     # Каждая ссылка должна быть уникальна (Можно было не Exception, а просто генерить свою)
            
            short_code = custom_alias

        else:               # Случайный вариант от сервиса

            while True:     # Делаю, пока не получу уникальный short_code (кол-во комбинаций алфавита и цифр для 6ти элементов ~2.1*10^9 вариантов)
                short_code = random_link_generator()

                if not self.repo.get_by_code(short_code):
                    break
        
        expires_dt = datetime.now(timezone.utc) + relativedelta(month=1)    # Все ссылки истекают спустя месяц после создания

        link = Link(
            orig_url=orig_url,
            short_code=short_code,
            expires_dt=expires_dt,
            user_id=user_id,
            project=project
        )

        return self.repo.create(link)


    def resolve_link(self, short_code):
        """Изменение инфо о ссылке (обращения к ней)"""

        cached = cache.get(short_code)
        if cached:
            return cached

        link = self.repo.get_by_code(short_code)
        if not link:
            return None
        
        if link.expires_dt and link.expires_dt.replace(tzinfo=timezone.utc) >= datetime.now(timezone.utc):    # Удаление ссылки по истечению срока хранения
            self.repo.delete(link)
            return None

        # Взаимодействия с ссылкой
        link.click_cnt += 1
        link.last_accessed_dt = datetime.now(timezone.utc)

        # Обновление инфо в таблице
        self.repo.update(short_code, link.orig_url)
        cache.set(short_code, link.orig_url)

        return link.orig_url
    

    def delete_link(self, short_code, user_id):
        """Удаление инфо о ссылке"""

        link = self.repo.get_by_code(short_code)
        if not link:
            return None
        
        self.check_owner(link, user_id)     # Проверка на логин

        cache.delete(short_code)
        self.repo.delete(link)

        return True
    

    def update_link(self, short_code: str, new_url: str, user_id):
        """Обновление инфо о ссылке"""

        link = self.repo.get_by_code(short_code)
        if not link:
            return None
        
        self.check_owner(link, user_id)
        link_upd = self.repo.update(short_code, new_url)
        cache.delete(short_code)

        return link_upd
    

    def search_links(self, orig_url: str):
        """Поиск алиаса по оригинальному url"""
        return self.repo.get_by_original(orig_url)
    

    def search_project(self, project: str):
        """Группировка алиасов по проектам"""
        return self.repo.get_by_project(project)
    

    def check_owner(self, link, user_id):
        """Проверка на доступность посылки для пользователя"""

        if link.user_id is None:
            raise Exception("Guest links cannot be modified")

        if link.user_id != user_id:
            raise Exception("Not owner")