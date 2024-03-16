import random
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from books.models import Book, Category
from books.serializers import BookSerializer, CategorySerializer

# Create your views here.

'''
Реализовать ручки каталога.
    - Получение всех книг.
    - Получение всех книг определенной категории.
    - Получение категорий текущего уровня и на 1 ниже.
    - Получение конкретной книги.
'''

@api_view(['GET'])
def get_all_books_view(request):
    '''Получение всех книг'''
    
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    
    return Response(
        {
            'success': True,
            'books': serializer.data
        }, status=status.HTTP_200_OK 
    )
        
@api_view(['GET'])
def get_books_one_category_view(request, category_id):
    ''' Получение всех книг определенной категории '''
    
    category = Category.objects.get(id=category_id)
    books = Book.objects.filter(categories=category)
    serializer = BookSerializer(books, many=True)
        
    return Response(
        {
            'success': True,
            'books': serializer.data
        }, status=status.HTTP_200_OK 
    )
    
@api_view(['GET'])
def get_current_category_view(request, category_id):
    ''' Получение категорий текущего уровня и на 1 ниже'''
    
    # книги категории и книг подкатегории 
    
    category = Category.objects.get(id=category_id) # Категории по id
    subcategories = Category.objects.filter(title=category) # Подкатегории по категории
    
    if subcategories.exists():
        # книги по данной категории + книги по подкатегориям
        books = Book.objects.filter(Q(categories=category), Q(categories=subcategories))
    
    # книги по данной категории
    books = Book.objects.filter(categories=category)
    serializer = BookSerializer(books, many=True)
    
    return Response(
            {
                'success': True,
                'books': serializer.data
            }, status=status.HTTP_200_OK 
        )
    
@api_view(['GET'])
def get_book_view(request, book_id):
    ''' Получение конкретной книги '''
    
    ''' На странице одной книги передавать список из 5 книг, которые находятся в той же категории'''
    try:
        book = Book.objects.get(id=book_id)
        book_serializer = BookSerializer(book)
        
        # найти категорию книги
        target_category = book.categories
        
        # если категорий больше одной
        if len(target_category) > 1:
            
            target_category = random.choices(target_category)
            
        # если категорий больше одной
        elif len(target_category) == 1:
            
            # найти 5 книг с той же категорией исключая текущую
            same_category_books = Book.objects.filter(
                categories=target_category).exclude(id=book_id)[:5]
            
        return Response(
            {
                'success': True,
                'book': book_serializer.data,
                'same_category_books': same_category_books,
            }, status=status.HTTP_200_OK 
        )
    except Book.DoesNotExist:
        return Response(
            {
                'message': 'У нас нет такой книги'
            }, 
            status = status.HTTP_404_NOT_FOUND
        )

# Class based views
class ListBooks(APIView):
    """ View для получения списка всех книг """
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Book.objects.all()
        
        title = self.request.query_params.get('title')
        author = self.request.query_params.get('author')
        status = self.request.query_params.get('status')
        
        if title is not None:
            queryset = queryset.filter(book__title=title)
            
        if author is not None:
            queryset = queryset.filter(book__author=author)
            
        if status is not None:
            queryset = queryset.filter(book__status=status)
        
        return queryset
    
    # def get(self, request, format=None):
    #     books = [book.name for book in Book.objects.all()]
    #     return Response(books)
    
class BookList(generics.ListAPIView):
    """ View для получения списка всех книг с фильтрацией по названию, автору, статусу и дате публикации """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'author', 'status', 'publication_date']
    

class SingleBookView(generics.RetrieveAPIView):
    """ View для получения одной книги  """
    
    ''' На странице одной книги передавать список из 5 книг, которые находятся в той же категории'''
    queryset = Book.objects.all()
    serializer_class = BookSerializer

'''
1. Фильтрация по названию
2. Фильтрация по автору
3. Фильтрация по статусу
4. Фильтрация по дате
5. На странице одной книги передавать список из 5 книг, которые находятся в той же категории
'''