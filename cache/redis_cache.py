import redis
from config import settings


class RedisCache:
    """Кэш редис-клиента"""

    def __init__(self):
        self.client = redis.Redis.from_url(settings.REDIS_URL)


    def get(self, key: str):
        """Обращение к клиенту"""

        value = self.client.get(key)
        if value:
            return value.decode()
        return None


    def set(self, key: str, value: str, ttl=3600):
        """Изменение таблицы"""
        self.client.setex(key, ttl, value)

    def delete(self, key: str):
        """Удаление инфо"""
        self.client.delete(key)


cache = RedisCache()