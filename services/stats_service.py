class StatsService:
    """Сервис для статистики обращений"""

    def __init__(self, repo):
        self.repo = repo

    def get_stats(self, short_code):

        link = self.repo.get_by_code(short_code)

        if not link:
            return None

        return {
            "orig_url": link.orig_url,
            "created_dt": link.created_dt,
            "click_cnt": link.click_cnt,
            "last_accessed_dt": link.last_accessed_dt
        }   # Статистика по конкретной ссылке