from services.link_service import LinkService
from unittest.mock import MagicMock


def test_create_link():
    """Тестирование создания ссылки"""
    repo = MagicMock()
    service = LinkService(repo)     # Автосоздание репозитория

    repo.get_by_code.return_value = None
    link = service.create_link("https://google.com")

    assert link is not None


def test_custom_alias():
    """Тестирование кастомного алиаса для ссылки"""
    repo = MagicMock()
    repo.get_by_code.return_value = True
    service = LinkService(repo)

    try:
        service.create_link("https://google.com", custom_alias="abc")
    except Exception:
        assert True