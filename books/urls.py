from django.urls import path
from books.views import (
    get_all_books_view,
    get_books_one_category_view, 
    get_current_category_view,
    get_book_view,
    BookList,
    SingleBookView
    )

app_name = "books"

urlpatterns = [
    path('api/books', BookList.as_view(), name='list_books'),
    path('api/books/<int:pk>', SingleBookView.as_view(), name='list_books'),
    
    
    
    # path('api/books', get_all_books_view, name='all_books'),
    path('api/<int:category_id>', get_books_one_category_view, name='get_books_one_category'),
    path('api/category/<int:category_id>/', get_current_category_view, name='get_current_category'),
    path('api/<int:book_id>', get_book_view, name='get_book'),
]