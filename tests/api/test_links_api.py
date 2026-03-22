def get_token(client):
    """Регистрация и авторизация (посылка)"""
    client.post(
        "/auth/register",
        json={
            "email": "user@mail.com",
            "password": "123456"
        }
    )   # Регистрация

    r = client.post(
        "/auth/login",
        json={
            "email": "user@mail.com",
            "password": "123456"
        }
    )   # Авторизация

    return r.json()["access_token"]     # доступ успешный


def test_create_link(client):
    """Создание короткой ссылки"""
    response = client.post(
        "/links/shorten",
        json={
            "orig_url": "https://google.com"
        }
    )
    assert response.status_code == 200  # Посылка успешна


def test_redirect(client):
    """Использование новой ссылки"""
    r = client.post(
        "/links/shorten",
        json={
            "orig_url": "https://google.com"
        }
    )

    code = r.json()["short_url"].split("/")[-1]
    response = client.get(f"/{code}")

    assert response.status_code == 307  # Временное перенаправление на сайт


def test_stats(client):
    """Получение статистики"""
    r = client.post(
        "/links/shorten",
        json={
            "orig_url": "https://google.com"
        }
    )

    code = r.json()["short_url"].split("/")[-1]
    response = client.get(f"/links/{code}/stats")

    assert response.status_code == 200  # Посылка успешна (вернулась статистика)


def test_update_link(client):
    """Обновление ссылки"""
    token = get_token(client)
    r = client.post(
        "/links/shorten",
        headers={"Authorization": f"Bearer {token}"},
        json={"orig_url": "https://google.com"}
    )

    code = r.json()["short_url"].split("/")[-1]
    response = client.put(
        f"/links/{code}",
        headers={"Authorization": f"Bearer {token}"},
        json={"orig_url": "https://openai.com"}
    )

    assert response.status_code == 200  # Успешно, ссылка обновилась


def test_delete_link(client):
    """Удаление ссылки"""
    token = get_token(client)
    r = client.post(
        "/links/shorten",
        headers={"Authorization": f"Bearer {token}"},
        json={"orig_url": "https://google.com"}
    )

    code = r.json()["short_url"].split("/")[-1]
    response = client.delete(
        f"/links/{code}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200