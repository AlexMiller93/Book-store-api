import os
from django.core.files import File
from django.db import models

from urllib import request


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
