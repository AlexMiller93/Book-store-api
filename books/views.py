from django.http import JsonResponse
from rest_framework import viewsets, filters
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
    search_fields = ['title']
    pagination_class = CustomPagination
    
    
    ' Метод для получения всех книг определенной категории и ее подкатегорий при наличии'
    @action(detail=True, serializer_class=BookSerializer)
    def get_books_category_sub(self, request, pk=None):
        
        # найти категорию книги по pk 
        try:
            category=self.get_object()
        # category=Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Категория не найдена."}, status=404)
        
        # подкатегории по категории
        subcategories = self.queryset.filter(subcategory=category) 
        
        if subcategories.exists():
            # книги по данной категории + книги по подкатегориям
            query_books = Book.objects.filter(Q(categories=category), Q(categories=subcategories))
            
        else:
            # Получение книг по категории
            query_books = Book.objects.filter(categories=category) 
        
        # # Получение книг по категории
        # query_books = Book.objects.filter(categories=category) 
        
        serializer = self.get_serializer(query_books, many=True)
        
        return Response(serializer.data)
        # return Response({'books': query_books})
    

class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """ Viewset для получения списка всех книг и одной книги """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title', 'authors', 'status', 'publication_date', 'categories']
    search_fields = ['title']
    pagination_class = CustomPagination
    
    ''' Список книг из одной категории'''
    @action(methods=['GET'], detail=False, url_path='by_category/(?P<category_name>[^/]+)')
    def get_by_category(self, request, category_name):
        category = Category.objects.filter(title__iexact=category_name).first()
        if not category:
            books = []
        else:
            books = self.queryset.filter(categories=category.id)
        page = self.paginate_queryset(books)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    
    ''' На странице одной книги передается список не менее из 5 книг, которые находятся в той же категории'''
    @action(detail=True)
    def get_books_same_category(self, request, pk=None):
        
        # найти категорию книги по pk 
        try:
            target_category = self.get_object()
        # target_category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Категория не найдена."}, status=404)

        # category = Category.objects.get(title=target_category)
        
        # не менее 5 книг с такой же категорией 
        same_category_books = Book.objects.filter(
            categories=target_category)
        
        serializer = self.get_serializer(same_category_books, many=True)
        
        return Response(serializer.data)
        # return JsonResponse({'books': same_category_books})
    
'''
1. Фильтрация по названию
2. Фильтрация по автору
3. Фильтрация по статусу
4. Фильтрация по дате
5. На странице одной книги передавать список из 5 книг, которые находятся в той же категории
'''