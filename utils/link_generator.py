import string, random


def random_link_generator(length=6):
    """Сгенерировать короткую ссылку (по дефолту 6 значений)"""
    alphabet = string.ascii_letters + string.digits     # Создаю полный алфавит из всех букв в кодировке и цифр 
    return "".join(random.choice(alphabet) for _ in range(length))      # Случайный набор из 6 элементов алфавита