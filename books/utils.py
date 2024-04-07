from typing import List


def clean_string(input_str: str) -> str | None:

    """
    Функция убирает лишние пробелы из строки
    и заменяет двойной дефис на одинарный,
    возвращает очищенную строку
    """

    if not input_str:
        return None

    # удаление лишних пробелов
    words = input_str.split()  # список из слов
    formatted_str = ' '.join(words)   # строка без лишних пробелов
    # замена двойного дефиса на одинарный
    formatted_str = formatted_str.replace("--", "-")
    return formatted_str


def clean_authors(authors: List[str]) -> List[str]:

    """
    Функция проверяет нахождение слова 'with' в элементе списка,
    разбивает строку на две составляющих,
    возвращает список с 2 строками без пробелов
    """

    def _clean():
        for item in authors:
            if 'with' in item:
                author_1, author_2 = item.split('with')
                yield author_1.strip()
                yield author_2.strip()
            elif item:  # если не пустая строка
                yield item
    return list(_clean())


def clean_isbn(isbn: str) -> str | None:

    """
    Функция проверяет если в isbn все символы цифры
    возвращает строку или None
    """

    if not isbn:
        return None
    result = ''.join(char for char in isbn if char.isdigit())
    if len(result) not in (10, 13):
        return None
    return result


def clean_page_number(raw_pages_number: str) -> int | None:

    try:
        pages_number = int(raw_pages_number)
    except ValueError:
        return None
    if pages_number <= 0:
        return None
    return pages_number
