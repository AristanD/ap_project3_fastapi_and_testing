from utils.link_generator import random_link_generator


def test_random_link_len():
    """Тестирование на проверку длину генерируемой ссылки"""
    code = random_link_generator()
    assert len(code) == 6   # Должен получаться 6-значный


def test_random_link_unique():
    """Тест на уникальность генерируемой ссылки
    Кол-во уникальных вариаций ~2.1*10^9. 
    Поэтому в силу ЗБЧ при небольшом количестве попыток доля уникальных результатов будет достигать хотя бы 90%
    """
    codes = set()

    for _ in range(1000):   # Прогоняю 1к раз
        codes.add(random_link_generator())
    
    assert len(codes) > 900     # Хотя бы 901 должны получиться уникальные (даже преуменьшил)