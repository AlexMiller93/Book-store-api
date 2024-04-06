from typing import Dict

from django.core.management.base import BaseCommand

from books.models import Book, Author, Category
from books.utils import (
    clean_page_number,
    clean_authors,
    clean_isbn,
    clean_string,
    )
from books.parsers import parse_json_from_url
from core.settings import URL


class Command(BaseCommand):
    help = 'Загрузка данных с обработкой в базу данных по ссылке'

    def handle(self, *args, **kwargs):
        try:

            json_data = parse_json_from_url(URL)

            # заведем словари авторов и категорий для проверки
            # на дубликат во время записи в БД

            known_authors: Dict[str, Author] = {}
            known_categories: Dict[str, Category] = {}

            for item in json_data:

                # парсинг данных из json файла
                title = item.get('title')

                raw_isbn = item.get('isbn')
                isbn = clean_isbn(raw_isbn)

                raw_pages_number = item.get('pageCount')
                pages_number = clean_page_number(raw_pages_number)

                publication_date = item.get('publishedDate')
                image_link = item.get('thumbnailUrl')
                if not image_link:
                    image_link = None

                summary = clean_string(item.get('shortDescription'))
                description = clean_string(item.get('longDescription'))
                status = item.get('status')

                # TODO: загрузка изображения

                # создание экземпляра книги без авторов и категорий
                book = Book.objects.create(
                    title=title,
                    isbn=isbn,
                    pages_number=pages_number,
                    publication_date=publication_date,
                    image_link=image_link,
                    summary=summary,
                    description=description,
                    status=status,
                )

                # обработка списка авторов
                author_names = clean_authors(item.get('authors', []))
                for author_name in author_names:
                    # переводим строку в формат для сравнения
                    casefold_author_name = author_name.casefold()

                    # находим автора в словаре уникальных авторов
                    author = known_authors.get(casefold_author_name)
                    if author is None:
                        # если данного автора не было в словаре,
                        # то создаем объект автора
                        author = Author.objects.create(name=author_name)

                        # заводим имя автора в словарь для проверки на дубликат
                        known_authors[casefold_author_name] = author

                    # добавляем автора к авторам книги
                    book.authors.add(author)

                # обработка списка категорий

                # удаление пустых элементов из списка
                category_names = list(filter(None, item.get('categories', [])))
                # если у книги нет категории, то задаем категорию Новинки
                if not category_names:
                    category_names = ['Новинки']

                for category_name in category_names:

                    # переводим строку в формат для сравнения
                    casefold_category_name = category_name.casefold()

                    # находим категорию в словаре уникальных категорий
                    category = known_categories.get(casefold_category_name)
                    if category is None:
                        # если данной категории не было в словаре,
                        # то создаем объект категории
                        category = Category.objects.create(title=category_name)

                        # заводим категорию в словарь для проверки на дубликат
                        known_categories[casefold_category_name] = category

                    # добавляем автора к авторам книги
                    book.categories.add(category)

                # сохраняем объект книги
                book.save()

            # вывод об успешной загрузке данных в БД
            self.stdout.write(self.style.SUCCESS(
                "Данные успешно загружены в базу!"))

        # отображение ошибки в случае сбоя загрузки
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Произошла ошибка: {e}'))
