from locust import HttpUser, task, between


class LinkUser(HttpUser):
    """Нагрузочный тест с Locust"""

    wait_time = between(1, 3)   # Жду 1-3 секунды

    @task
    def create_link(self):
        """Множественно создаю ссылки"""
        self.client.post(
            "/links/shorten",
            json={
                "orig_url": "https://google.com"
            }
        )

    @task
    def redirect(self):
        """Перенаправление на ссылку"""
        self.client.get("/gh")