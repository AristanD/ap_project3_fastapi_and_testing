def test_register(client):
    """Тест регистрации"""
    response = client.post(
        "/auth/register",
        json={
            "email": "test@mail.com",
            "password": "123456"
        }
    )
    assert response.status_code == 200  # Ожидаемый результат посылки - всё отработало успешно


def test_login(client):
    """Тестирование регистрации и авторизации вместе"""
    client.post(
        "/auth/register",
        json={
            "email": "test@mail.com",
            "password": "123456"
        }
    )   # Регистрация

    response = client.post(
        "/auth/login",
        json={
            "email": "test@mail.com",
            "password": "123456"
        }
    )   # Авторизация

    assert "access_token" in response.json()    # Ожидаемый результат - совпадение хэшей пароля в БД и с посылки + логин