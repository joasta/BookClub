from bookclass import Book
from bookclass import Reader

class Intern:
    readers=[]
    books=[]
    _command=""
    _name=""
    _rest=""

    def __init__(self, name):
        self._name = name
        self.read_readers()
        self.read_books()

    def read_readers(self):
        with open('reader.txt', 'r') as f:
            f1 = f.readlines()
            for ele in f1:
                a_read = Reader(*ele.split("|"))
                self.readers.append(a_read)
    def read_books(self):
        with open('book.txt', 'r') as f:
            f1 = f.readlines()
            for ele in f1:
                a_book = Book(*ele.split("|"))
                self.books.append(a_book)

    def save_readers(self):
        with open('reader.txt', 'w') as f:
            for ele in self.readers:
                a_line = str(ele.title) + "|" + str(ele.username) + "|" + str(ele.rating) + "\n"
                f.write(a_line)

    def save_books(self):
        with open('book.txt', 'w') as f:
            for ele in self.books:
                a_line = str(ele.title) + "|" + str(ele.author) + "|" + str(ele.genre) + "|" + str(ele.link)
                a_line += "|" + str(ele.username) + "|" + str(ele.rating) + "\n"
                f.write(a_line)

    def rates(self, a_read):
        users_book = [r for r in self.readers if (r.title == a_read.title and r.username == a_read.username)]
        if not users_book:
            self.readers.append(a_read)
        else:
            for r in self.readers:
                if (r.title == a_read.title and r.username == a_read.username):
                    r = a_read
              
        rated = [int(r.rating) for r in self.readers if r.title == a_read.title]
        average = sum(rated)
        
        for b in self.books:
            if (b.title == a_read.title):
                b.rating = "{:.2f}".format(average)
        
        self.save_readers()
        self.save_books()
        return True

    def print_rec(self, a_book, comment):
        a_read = Reader(a_book.title, a_book.username, a_book.rating)
        for book in self.books:
            if book.title == a_book.title:
                print("The book is already on the list! I'll add it to your library card.")
                self.rates(a_read)
                return True

        print(f"""\nNew recommendation by {a_book.username}!
        Genre: {a_book.genre}
        Title: {a_book.title}
        Author: {a_book.author}
        Link to description: {a_book.link}
        Commentary: {comment}""")

        self.books.append(a_book)

        self.rates(a_read)
        return True

    def rate_book(self, a_read):
        if_book = [b for b in self.books if b.title == a_read.title]

        if not if_book:
            print("I don't know that book. Recommend it first!")
            return False
        else:
            rates(a_read)

    def get_rec_user(self, user):
        if_user = [r for r in self.readers if r.username == user]
        if not if_user:
            print("There's no library card under such a name.")
            return False

        users_books = [r.title for r in if_user if int(r.rating) >= 2.5]
        if not users_books:
            print("I have no books to recommend.")
            return False

        read_books = [r.title for r in self.readers if r.username == self._name]

        recs = [i for i in users_books if i not in read_books]
        if not recs:
            print("I have nothing to recommend.")
            return False

        recommended = recs[randint(0, len(recs)-1)]
    
        the_one = [b for b in self.books if b.title == recommended]
        the_one = the_one[0]
        print(f"""My recommendation:
        {the_one.title} by {the_one.author}
        added by {the_one.username}
        average rating: {the_one.rating}""")

        return True

    def get_rec_genre(self, instream):
        if_genre = [r.title for r in self.readers if instream in r.genre]
        if not if_genre:
            print("That section of our library is yet empty.")
            return False
        
        read_books = [r.title for r in self.readers if r.username == self._name]

        recs = [i for i in if_genre if i not in read_books]
        if not recs:
            print("I have nothing to recommend.")
            return False

        recommended = recs[randint(0, len(recs)-1)]
    
        the_one = [b for b in self.books if b.title == recommended]
        the_one = the_one[0]
        print(f"""My recommendation:
        {the_one.title} by {the_one.author}
        added by {the_one.username}
        average rating: {the_one.rating}""")

        return True

    def get_info(self, instream):
        the_one = [b for b in self.books if b.title == instream]

        if not the_one:
            print("I don't know this book.")
            return False
        
        the_one = the_one[0]

        print(f"""{the_one.title} by {the_one.author}
        genre: {the_one.genre}
        added by {the_one.name}
        average rating: {the_one.rating}
        see more: {the_one.link}""")

            
    def parse_rec(self, instream):
        title, author, genre = None, None, None
        link = ""
        rating = 5

        for ele in instream.split('>'):
            part = ele.split(" ", 1)[0]
            if part == "t":
                title = ele.split(' ', 1)[1]
            elif part == "a":
                author = ele.split(' ', 1)[1]
            elif part == "g":
                genre = ele.split(' ', 1)[1]
            elif part == "l":
                link = ele.split(' ', 1)[1]
            elif part == "r":
                rating = ele.split(' ', 1)[1]
            elif part == ".":
                self._rest = ele.split(' ', 1)[1]

        if title is None or author is None or genre is None:
            print("Wrong input format!")
            return False

        title = title.strip()
        author = author.strip()
        genre = genre.strip()
        link = link.strip()
        self._rest = self._rest.lstrip()

        try:
            rating.strip()
            rating = int(rating)
        except AttributeError:
            rating = 5
        except ValueError:
            rating = 5

        if rating > 5 or rating < 0:
            print("Wrong rating!")
            return False

        a_book = Book(title, author, genre, link, self._name, rating)
        self.print_rec(a_book, self._rest)

    def parse_rate(self, instream):
        title = None
        rating = None

        for ele in instream.split('>'):
            part = ele.split(' ', 1)[0]
            if part == t:
                title = ele.split(' ', 1)[1]
            elif part == r:
                rating = ele.split(' ', 1)[1]

        if title is None or rating is None:
            print("Wrong input format!")
            return False

        title.strip()
        try:
            rating.strip()
            rating = int(rating)
        except ValueError:
            print("Wrong input format!")
            return False
        except AttributeError:
            rating = int(rating)

        if rating > 5 or rating < 0:
            print("Wrong rating!")
            return False

        a_read = Reader(title, self._name, rating)
        self.rate_book(a_read)

    def parse_text(self, instream):
        self._command, instream = instream.split(' ', 1)

        if self._command == "rec":
            self.parse_rec(instream)

        elif self._command == "rate":
            self.parse_rate(instream)

        elif self._command == "info":
            title = instream.strip()
            self.get_info(title)

        elif self._command == "getu":
            user = instream.strip()
            self.get_rec_user(user)

        elif self._command == "getg":
            genre = instream.strip()
            self.get_rec_genre(genre)

