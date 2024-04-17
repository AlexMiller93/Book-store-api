from django.urls import include, path
from rest_framework import routers

from books.views import CategoryViewSet, BookViewSet, FeedbackViewSet

router = routers.SimpleRouter()

router.register(r'books', BookViewSet, basename='books')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'feedback', FeedbackViewSet, basename='feedback')

# api/v1/books - все книги
# api/v1/books/{pk}/get_books_same_category
# - книга по ключу + 5 книг той же категории

# api/v1/categories - все категории
# api/v1/categories/{pk}/get_books_category_sub/
# - книги одной категории + книги из подкатегорий

# api/v1/feedback - все отзывы

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
