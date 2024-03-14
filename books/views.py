from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from books.models import Book, Category
from books.serializers import BookSerializer

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
    if request.method == 'GET':
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
    
    if request.method == 'GET':
        category = Category.objects.get(id=category_id)
        books = Book.objects.filter(categories=category)
        serializer = BookSerializer(books, many=True)
            
        return Response(
            {
                'success': True,
                'books': serializer.data
            }, status=status.HTTP_200_OK 
        )
        
def get_current_category():
    ''' Получение категорий текущего уровня и на 1 ниже'''
    categories = Category.objects.filter()
    return categories

def get_book(book_id):
    ''' Получение конкретной книги '''
    
    try:
        book = Book.objects.get(id=book_id)
        return book
    except Book.DoesNotExist:
        return Response(
            {
                'message': 'У нас нет такой книги'
            }, 
            status = status.HTTP_404_NOT_FOUND
        )
    