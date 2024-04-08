from django.test import TestCase
from books.models import Book, Author, Category


# Create your tests here.


class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Book.objects.create(title='Test book', isbn='1234567890', pages_number=100)

    def test_max_length_isbn(self):
        book=Book.objects.get(id=1)
        max_length = book._meta.get_field('isbn').max_length
        self.assertEquals(max_length,13)
    
class CategoryModelTest(TestCase):
    pass


""" 
class BookTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title='Test book', isbn='1234567890')
        self.author = Author.objects.create(name='Test author')
        self.category = Category.objects.create(title='Test category')
        
        # self.book.authors.add(self.author)
        # self.book.authors.add(self.category)
        # self.book.save()
        
    def test_model_str(self):
        self.assertEqual(str(self.author), 'Test author')
        self.assertEqual(str(self.category), 'Test category')
        # self.assertEqual(str(self.book), f'Книга: {self.book.title} автора {self.book.authors} с категорией {self.book.categories}')
        # self.assertEqual(str(self.book), 'Книга: Test book автора Test author с категорией Test category')
        
    def tearDown(self):
        pass
"""