from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255, help_text='Имя автора книги')
    
    class Meta:
        ordering = ["name"]
        verbose_name='Автор'
        verbose_name_plural = 'Авторы'
    
    def __str__(self):
        return self.name

class Category(models.Model):
    title = models.CharField(max_length=255, blank=True, help_text='Наименование категории книг')
    subcategory = models.ForeignKey(
        'self', 
        null=True,
        blank=True, 
        on_delete=models.CASCADE,
        help_text='Наименование подкатегории книг')
    
    class Meta:
        ordering = ["title"]
        verbose_name='Категория'
        verbose_name_plural = 'Категории'
        
    def __str__(self):
        return self.title
    
class Book(models.Model):
    
    BOOK_STATUS = (
        ('P', 'PUBLISH'), # True
        ('M', 'MEAP'), # false
    )
        
    title = models.CharField(max_length=255, help_text='Название книги', )
    isbn = models.CharField(max_length=255, help_text='Код ISBN')
    pages_number = models.PositiveIntegerField(blank=True, help_text='Количество страниц в книге') # 0 -> None
    publication_date = models.DateField(blank=True, help_text='Дата публикации книги')
    image_link = models.URLField(blank=True, help_text='Ссылка на фото книги')
    image = models.ImageField(blank=True, upload_to=f'{isbn}/', help_text='Фотография книги')
    summary = models.TextField(blank=True, help_text='Описание книги')
    description = models.TextField(blank=True, help_text='Подробное описание книги')
    status = models.CharField(max_length=8, help_text='Статус книги')
    
    authors = models.ManyToManyField(
            Author, 
            # through_fields=("book", "author"), 
            related_name='authors',
        )
    
    categories = models.ManyToManyField(
            Category, 
            # through_fields=("book", "category"),
            related_name='categories',
        )
    
    class Meta:
        ordering = ["title", "isbn"]
        verbose_name_plural = 'Книги'
        
    def __str__(self):
        return f'Книга: {self.title} автора {self.authors} с категорией {self.categories}'

