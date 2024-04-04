from django.contrib import admin

from books.models import Book, Category, Author
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'subcategory']
    ordering = ('title',)
    search_fields = ('title', 'subcategory')

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ('name',)
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'isbn', 'pages_number', 'publication_date', 'image_link', 'summary', 'description', 'status']
    ordering = ('title', 'isbn', 'authors', 'categories')
    search_fields = ('title', 'isbn', 'publication_date', 'status')


# class BookResource(resources.ModelResource):
#     class Meta:
#         model = Book
        
# class BookAdmin(ImportExportModelAdmin):
#     resource_class = BookResource

# admin.site.register(Book,BookAdmin)