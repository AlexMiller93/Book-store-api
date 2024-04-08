import os
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import models

from urllib import request

from PIL import Image
import requests



class Author(models.Model):
    """ Модель Автор с полем имя """
    name = models.CharField(max_length=255, help_text='Имя автора книги')

    class Meta:
        ordering = ["name"]
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return self.name


class Category(models.Model):
    """ Модель Категория с полями название и подкатегория """

    title = models.CharField(
        max_length=255, blank=True, help_text='Наименование категории книг'
        )
    subcategory = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text='Дочерняя категория книг')

    class Meta:
        ordering = ["title"]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Book(models.Model):
    """
        Модель Категория с полями:
            название, isbn, количество страниц, дата публикации,
            ссылка на фото, фотография, краткое описание, подробное описание,
            статус, авторы, категории

        метод get_remote_image для сохранения фотографий в БД по url
    """
    title = models.CharField(max_length=255, help_text='Название книги', )
    isbn = models.CharField(
        max_length=13, help_text='Код ISBN', null=True, blank=True)
    pages_number = models.PositiveIntegerField(
        blank=True, null=True, help_text='Количество страниц в книге')
    publication_date = models.DateField(
        blank=True, null=True, help_text='Дата публикации книги')
    image_link = models.URLField(
        blank=True, null=True, help_text='Ссылка на фото книги')
    image = models.ImageField(
        blank=True, null=True, upload_to=f'images/{isbn}/',
        help_text='Фотография книги')
    summary = models.TextField(
        blank=True, null=True, help_text='Описание книги')
    description = models.TextField(
        blank=True, null=True, help_text='Подробное описание книги')
    status = models.CharField(max_length=8, help_text='Статус книги')

    authors = models.ManyToManyField(
            Author,
            related_name='authors',
        )

    categories = models.ManyToManyField(
            Category,
            related_name='categories',
        )

    class Meta:
        ordering = ["title", "publication_date"]
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return f"""Книга: {self.title} автора {self.authors}
                    с категорией {self.categories}"""

    def authors_as_text(self):
        return " | ".join(self.authors.values_list("label", flat=True))

    def categories_as_text(self):
        return " | ".join(self.categories.values_list("label", flat=True))

    # метод для сохранения фотографий в БД по url
    def get_remote_image(self):
        if self.image_link and not self.image:
            result = request.urlretrieve(self.image_link)
            self.image.save(
                os.path.basename(self.image_link),
                File(open(result[0], 'rb'))
            )
            self.save()

    # TODO: возможно стоит перенести загрузку фото в commands
    def download_image_from_url(book):
        # Проверяем, что у книги есть ссылка на изображение
        if book.image_url:
            try:
                # Получаем содержимое изображения по ссылке
                response = requests.get(book.image_link)
                response.raise_for_status()  # Проверяем успешность запроса

                # Создаем временный файл для сохранения изображения
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(response.content)
                img_temp.flush()

                # Открываем изображение с помощью Pillow для обработки
                img = Image.open(img_temp.name)

                # Проверяем и, если необходимо, изменяем размер изображения
                max_width = 800
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((max_width, new_height), Image.ANTIALIAS)

                # Сохраняем изображение на локальную машину
                img_path = os.path.join(
                    'media', 'book_images', f'{book.pk}.jpg')
                img.save(img_path)

                # Обновляем поле изображения модели книги
                book.image.save(
                    f'{book.pk}.jpg', File(open(img_path, 'rb')), save=True)

                # Удаляем временный файл
                img_temp.close()

                return True  # Возвращаем True, если загрузка прошла успешно
            except Exception as e:

                print(f"""Возникла ошибка при загрузке изображения
                    для книги {book.pk}: {e}""")
                return False  # Возвращаем False в случае ошибки загрузки
        else:
            print(f"Нет ссылки для загрузки изображения книги {book.pk}")

            # Возвращаем False, если у книги нет ссылки на изображение
            return False
