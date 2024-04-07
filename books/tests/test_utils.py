import random
import string
from books import utils


# Create your tests here.

# tests function clean_string

def test_clean_string_empty():
    s = ''
    assert utils.clean_string(s) is None
    
def test_clean_string_change_symbols():
    test_str = '   -- abc  abc   '
    assert utils.clean_string(test_str) == '- abc abc'

def test_clean_string_correct():
    test_str = '   abc  abc  abc   '
    assert utils.clean_string(test_str) == 'abc abc abc'

# tests function clean_authors

def test_clean_authors_empty():
    author = ['Test author']
    assert utils.clean_isbn(author) is None

def test_clean_authors_correct():
    authors = ['Test 1 with Test 2', 'Test 3']
    assert utils.clean_authors(authors) == ['Test 1', 'Test 2', 'Test 3']

# tests function clean_isbn

def test_clean_isbn_empty():
    s = ''
    assert utils.clean_isbn(s) is None
    
def test_clean_isbn_wrong_length():
    random_num = random.randint(3,9)
    lst = [random.choice(string.digits) for _ in range(random_num)]
    chars = ''.join(lst)
    assert utils.clean_isbn(chars) is None

def test_clean_isbn_correct():
    chars = ''.join([random.choice(string.digits) for _ in range(10)])
    assert utils.clean_isbn(chars) == chars

# tests function clean_page_number

def test_clean_page_number_not_a_number():
    s = "abcd"
    assert utils.clean_page_number(s) is None


def test_clean_page_number_zero():
    s = "0"
    assert utils.clean_page_number(s) is None


def test_clean_page_number_negative():
    s = "-1"
    assert utils.clean_page_number(s) is None


def test_clean_page_number_correct():
    s = "123"
    assert utils.clean_page_number(s) == 123






