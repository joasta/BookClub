import pytest
import io
import contextlib

from Intern import Intern
from BookObjects import Book, Reader

#@pytest.fixture
#def new_intern():
#    return Intern("new user")

@pytest.mark.parametrize(
    'title, link, rate, expected, expected2',
    [
        ('>t Book 3', "", "", 'tests/book1.txt', 'tests/reader1.txt'),
        ('>t Book', "", "", 'tests/book2.txt', 'tests/reader2.txt'),
        ('>t Book', "", ">r 3", 'tests/book3.txt', 'tests/reader3.txt'),
        ('>t Book 4', ">l eoeo", ">r 3.5", 'tests/book4.txt', 'tests/reader4.txt'),
        ("Book", " ", " ", 'tests/book4.txt', 'tests/reader4.txt')
    ]
)
def test_add_new_book(title, link, rate, expected, expected2):
    new_intern = Intern("new user")
    new_intern.parse_text(f"rec {title} >a NA >g NA {link} {rate}")
    
    with open('book.txt') as generate:
        with open(expected) as expect:
            assert generate.read() == expect.read()
            
    with open('reader.txt') as generate:
        with open(expected2) as expect:
            assert generate.read() == expect.read()

@pytest.mark.parametrize(
    'title, rate, expected, expected2',
    [
        ('>t Book 3', "", 'tests/book4.txt', 'tests/reader4.txt'),
        ('>t Book 2', ">r 4", 'tests/book4.txt', 'tests/reader4.txt'),
        ('>t Book 3', ">r 3.2", 'tests/book5.txt', 'tests/reader5.txt'),
        ('>t Book 5', ">r 3.6", 'tests/book6.txt', 'tests/reader6.txt')
    ]
)
def test_add_new_rating(title, rate, expected, expected2):
    new_intern = Intern("new user")
    new_intern.parse_text(f"rate {title} {rate}")
    
    with open('book.txt') as generate:
        with open(expected) as expect:
            assert generate.read() == expect.read()
            
    with open('reader.txt') as generate:
        with open(expected2) as expect:
            assert generate.read() == expect.read()

@pytest.mark.parametrize(
    'title, expected',
    [
        ('Book', """Book by May Parker
        genre: poetry
        added by jess
        average rating: 3.50
        see more: www\n"""),
        ('Books', "I don't know this book.\n")
    ]
)
def test_get_info(title, expected):
    f = io.StringIO()
    new_intern = Intern("new user")
    with contextlib.redirect_stdout(f):
        new_intern.parse_text(f"info {title}")
    assert expected == f.getvalue()
    
@pytest.mark.parametrize(
    'username, expected',
    [
        ('jay', "I have no books to recommend.\n"),
        ('kay', "There's no library card under such a name.\n"),
        ('jess', """My recommendation:
        Book 1 by Ben Parker
        added by jess
        average rating: 3.50\n\n""")
    ]
)
def test_get_user_recommendations(username, expected):
    f = io.StringIO()
    new_intern = Intern("new user")
    with contextlib.redirect_stdout(f):
        new_intern.parse_text(f"getu {username}")
    assert expected == f.getvalue()
    
@pytest.mark.parametrize(
    'user, genre, expected',
    [
        ('new', 'fantasy', """My recommendation:
        Book 1 by Ben Parker
        added by jess
        average rating: 3.50\n\n"""),
        ('new', 'comic', "That section of our library is yet empty.\n"),
        ('new', 'romance', """My recommendation:
        Book 5 by Arthur Pendragon
        added by joy
        average rating: 4.20\n\n"""),
        ('new user', 'romance', "I have nothing to recommend.\n")
    ]
)
def test_get_genre_recommendations(user, genre, expected):
    f = io.StringIO()
    new_intern = Intern(user)
    with contextlib.redirect_stdout(f):
        new_intern.parse_text(f"getg {genre}")
    assert expected == f.getvalue()

def test_bring_it_back():
    intern = Intern("tmp")

    book1 = Book('Book','May Parker','poetry','www','jess','4.00')
    book2 = Book('Book 1','Ben Parker','fantasy','www','jess','3.50')
    book3 = Book('Book 5','Arthur Pendragon','science-fiction, romance','www','joy','4.50')

    intern.books = [book1, book2, book3]
    intern.save_books()
    
    read1 = Reader('Book','jess','4.00')
    read2 = Reader('Book 1','jess','5.00')
    read3 = Reader('Book 1','jay','2.00')
    read4 = Reader('Book 5','joy','5.00')
    read5 = Reader('Book 5','jo','4.00')
    
    intern.readers = [read1, read2, read3, read4, read5]
    intern.save_readers()