import json

from django.core.management.base import BaseCommand

from books.models import Book, Author, Category
from books.utils import (
    divide_authors, 
    clean_string, 
    clean_list, 
    is_correct_isbn, 
    clean_date_format
    )


class Command(BaseCommand):
    help = 'Загрузка данных в базу данных из json файла'

    # !! https://metanit.com/python/django/5.7.php

    def handle(self, *args, **kwargs):
        try:
            # TODO: заменить на ссылку из гитлаба
            with open('data/books.json', 'r', encoding='utf8') as file:
                data = json.load(file)
                
                # for item in data:
                
                # item = data[0] # cat, authors - list of items
                
                item = data[9] # cat, authors - one item
                
                # парсинг данных из json файла
                title = item.get('title')
                
                raw_isbn=item.get('isbn')
                if is_correct_isbn(raw_isbn):
                    isbn = raw_isbn
                else:
                    isbn = 'Wrong isbn'
                
                pages_number = int(item.get('pageCount'))
                publication_date = clean_date_format(item.get('publishedDate')["$date"])
                image_link = item.get('thumbnailUrl')
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
                # ['', ''] - ['']
                
                # список авторов
                authors_data = clean_list(divide_authors(item.get('authors', []))) # list
                # 
                
                author_value = ''.join(authors_data)
                print(author_value)
                
                # if authors_data is not None:
                if len(authors_data) > 1:
                    author = [Author.objects.create(name=author) for author in authors_data]
                else:
                    author = Author.objects.create(name=authors_data)
                
                # список категорий
                categories_items = clean_list(item.get('categories', []))
                
                
                
                
                # if categories_items is not None:
                #     if len(categories_items) > 1:
                #         category = [Category.objects.create(title=category) for category in categories_items]
                #     else:
                #         category = Category.objects.create(title=categories_items) 
                # else:  
                #     category = 'New books'
                
                
                
                ''' 
                # создадим курс
                python = Course.objects.create(name="Python")
                
                # создаем студента и добавляем его на курс
                python.student_set.create(name="Bob")
                
                # отдельно создаем студента и добавляем его на курс
                sam = Student(name="Sam")
                sam.save()
                python.student_set.add(sam)
                
                # добавляем курс для студента bob
                bob.courses.add(django, through_defaults={"date": date.today(), "mark": 5})
                '''
                book_dict = {
                    'title': title,
                    'isbn': isbn,
                    'pages_number': pages_number,
                    'publication_date': publication_date,
                    'image_link': image_link,
                    'summary': summary,
                    'description': description,
                    'status': status
                }
                #! add -> 1   book.authors.add()
                #! set -> >1  book.authors.set()
                
                # сохраним объект
                book.save()
                print(f'Book object: {book}')
                print(f'Author object: {author}')
                # print(f'Category object: {category}\n')
                
                # book.authors.set(author) # for many queryset items
                # book.categories.set(category) # for many queryset items
                
                book.authors.add(author) # for one queryset item
                # book.categories.add(category) # for one queryset item
                
                book.save()
                # print(f'Book object after adding authors and cat: {book}')
                
                # if len(author) == 1:
                #     book.authors.add(author)
                # else:
                #     book.authors.set(author)
                
                # if len(category) == 1:
                #     book.categories.add(category)
                # else:  
                #     book.categories.set(category)
                
                
                
                # book.categories.add(category, through_defaults=book_dict)
                
            self.stdout.write(self.style.SUCCESS("Данные успешно загружены!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Произошла ошибка: {e}'))

#!! Ошибки при запуске: 
# ? Field 'id' expected a number but got ['W. Frank Ableson', 'Charlie Collins', 'Robi Sen'].

#!! Ошибки при создании, сохранении в БД:

# ? isbn - 'Wrong isbn'
# ? status  -- нет
#


# ! анализ books.json

# TODO: можно проверить код isbn на корректность составления


