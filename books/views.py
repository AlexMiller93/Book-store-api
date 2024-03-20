from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from books.models import Book, Category
from books.serializers import BookSerializer, CategorySerializer
from books.paginations import CustomPagination

# Class based views

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ Viewset для получения списка всех категорий и одной категории """
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'
    pagination_class = CustomPagination
    
    
    ' Метод для получения всех книг определенной категории и ее подкатегорий при наличии'
    @action(methods=['get'], detail=True)
    def get_books_category_sub(self, request, pk=None):
        
        # найти категорию книги по pk 
        category=self.get_object()
        # category=Category.objects.get(id=pk)
        
        # подкатегории по категории
        subcategories = Category.objects.filter(title=category) 
        
        if subcategories.exists():
            
            # книги по данной категории + книги по подкатегориям
            query_books = Book.objects.filter(Q(categories=category), Q(categories=subcategories))
            
        else:
            
            # Получение книг по категории
            query_books = Book.objects.filter(categories=category) 
            
        return Response({'books': query_books})
    

class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """ Viewset для получения списка всех книг и одной книги """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'authors', 'status', 'publication_date']
    pagination_class = CustomPagination
    
    ''' На странице одной книги передается список не менее из 5 книг, которые находятся в той же категории'''
    @action(methods=['get'], detail=True)
    def get_books_same_category(self, request, pk=None):
        
        # найти категорию книги по pk 
        target_category = self.get_object()
        # target_category = Category.objects.get(pk=pk)
        
        # не менее 5 книг с такой же категорией 
        same_category_books = Book.objects.filter(
            categories=target_category).exclude(pk=pk)[:5]
        
        return Response({'books': same_category_books})
    
'''
1. Фильтрация по названию
2. Фильтрация по автору
3. Фильтрация по статусу
4. Фильтрация по дате
5. На странице одной книги передавать список из 5 книг, которые находятся в той же категории
'''