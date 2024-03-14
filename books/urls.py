from django.urls import path
from books.views import (
    get_all_books_view,
    get_books_one_category_view, 
    get_current_category,
    get_book
    )

urlpatterns = [
    path('all_books', get_all_books_view, name='all_books'),
    path('<int:category_id>', get_books_one_category_view, name='get_books_one_category'),
    path('category/<int:category_id>/', get_current_category, name='get_current_category'),
    path('<int:book_id>', get_book, name='get_book'),
]