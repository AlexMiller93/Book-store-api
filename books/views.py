from rest_framework import viewsets, filters
from rest_framework.decorators import action

from django_filters.rest_framework import DjangoFilterBackend

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


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """ Viewset для получения списка всех книг и одной книги """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = [
        'title', 'authors', 'status', 'publication_date', 'categories']
    search_fields = ['title']
    pagination_class = CustomPagination

    # @action(detail=True)
    # def get_books_same_category(self, request, pk=None):
    #     ''' На странице одной книги передается список не менее из 5 книг,
    #         которые находятся в той же категории'''

    #     # найти категорию книги по pk
    #     try:
    #         target_category = self.get_object()
    #     except Category.DoesNotExist:
    #         return Response({"error": "Категория не найдена."}, status=404)

    #     # category = Category.objects.get(title=target_category)

    #     # не менее 5 книг с такой же категорией
    #     same_category_books = Book.objects.filter(
    #         categories=target_category)

    #     serializer = self.get_serializer(same_category_books, many=True)

    #     return Response(serializer.data)

    @action(detail=False, url_path='by_category/(?P<category_name>[^/]+)')
    def get_by_category(self, request, category_name):
        ''' Список книг из одной категории'''

        return self._get_by_category(category_name, False)

    @action(
        detail=False,
        url_path='by_category/(?P<category_name>[^/]+)/subcategories')
    def get_by_category_with_children(self, request, category_name):
        ''' Список книг из одной категории и дочерних'''

        return self._get_by_category(category_name, True)

    def _get_by_category(
            self, category_name: str, include_parent_categories: bool = False):
        ''' Метод для отображения списка книг по категории
            и/или по дочерним категориям при их наличии '''

        category = Category.objects.filter(title__iexact=category_name).first()
        if not category:
            books = []
        else:
            # если у категории есть родитель
            if include_parent_categories:

                # находим родителя
                child_categories = Category.objects.filter(
                    subcategory_id=category.id).order_by('title')
                
                print(f'Child categories for category {category}: {child_categories}\n')

                # добавляем в список
                include_category_ids = [cat.id for cat in child_categories]
            else:
                include_category_ids = []

            # добавляем в список искомую категорию
            include_category_ids.append(category.id)

            books = self.queryset.filter(categories__in=include_category_ids)

        page = self.paginate_queryset(books)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(serializer.data)


'''
1. Фильтрация по названию
2. Фильтрация по автору
3. Фильтрация по статусу
4. Фильтрация по дате
5. На странице одной книги передавать список из 5 книг, которые находятся
в той же категории
'''
