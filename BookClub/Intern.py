from BookObjects import Book
from BookObjects import Reader
from random import randint

class Intern:
    """Connects the user with the library."""

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
        """Load members' opinions to a list of Readers."""

        with open('reader.txt', 'r') as f:
            f1 = f.readlines()
            for ele in f1:
                a_read = Reader(*ele.split("|"))
                self.readers.append(a_read)

    def read_books(self):
        """Load recommended books to a list of Books."""

        with open('book.txt', 'r') as f:
            f1 = f.readlines()
            for ele in f1:
                a_book = Book(*ele.split("|"))
                self.books.append(a_book)

    def save_readers(self):
        """Save current opinions to a readers' database."""

        with open('reader.txt', 'w') as f:
            for ele in self.readers:
                if isinstance(ele.rating, str): ele.rating = ele.rating.rstrip()
                a_line = str(ele.title) + "|" + str(ele.username) + "|" + str(ele.rating) + "\n"
                f.write(a_line)

    def save_books(self):
        """Save current recommendations to a books' database."""

        with open('book.txt', 'w') as f:
            for ele in self.books:
                if isinstance(ele.rating, str): ele.rating = ele.rating.rstrip()
                a_line = str(ele.title) + "|" + str(ele.author) + "|" + str(ele.genre) + "|" + str(ele.link)
                a_line += "|" + str(ele.username) + "|" + str(ele.rating) + "\n"
                f.write(a_line)

    def rates(self, a_read):
        """
        Update library cards with a new rating.

        Check if the user has already rated the book before;
        update or add his rating, accordingly.
        Calculate a new average rating from all saved ratings of the book.
        Save to databases: books and readers.

        Parameters:
            a_read - Reader object with a new rating
        """

        users_book = [r for r in self.readers if (r.title == a_read.title and r.username == a_read.username)]
        if not users_book:
            self.readers.append(a_read)
        else:
            for i, r in enumerate(self.readers):
                if (r.title == a_read.title and r.username == a_read.username):
                    self.readers[i] = a_read
              
        rated = [float(r.rating) for r in self.readers if r.title == a_read.title]
        average = sum(rated)/len(rated)
        
        for i, b in enumerate(self.books):
            if (b.title == a_read.title):
                b.rating = "{:.2f}".format(average)
        
        self.save_readers()
        self.save_books()

    def save_rec(self, a_book, comment):
        """
        Save new book recommendation.
        
        Check if the book is already in the library's records.
        If not, print out the recommendation and add a new
        record to books' database.
        Proceed to update of the book rating (function: rates).

        Parameters:
            a_book - Book object with complete new book's data
        """

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

    def rate_book(self, a_read):
        """
        Check if the rated book is known.
        
        Check if the rated book is in the library's records.
        If not, proceed to updating the rating (function: rates).

        Parameters:
            a_read - Reader object with a new rating
        """

        if_book = [b for b in self.books if b.title == a_read.title]

        if not if_book:
            print("I don't know that book. Recommend it first!")
            return False
        else:
            self.rates(a_read)

    def get_rec_user(self, user):
        """
        Recommend a book based on a username.

        Check if the requested username is saved in the records.
        If so, pick the books the requested user rated with 2.5
        and higher that hasn't been rated by a current user; pick
        a book at random and print out its data.

        Parameters:
            user - str containing a requested username
        """

        if_user = [r for r in self.readers if r.username == user]
        if not if_user:
            print("There's no library card under such a name.")
            return False

        users_books = [r.title for r in if_user if float(r.rating) >= 2.5]
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

    def get_rec_genre(self, genr):
        """
        Recommend a book based on a genre.

        Check if the requested genre is listed in the records.
        If so, pick the books from the genre that hasn't been
        rated by a current user; pick a book at random and
        print out its data.

        Parameters:
            genr - str naming a requested genre
        """

        if_genre = [r.title for r in self.books if genr in r.genre]
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

    def get_info(self, titl):
        """
        Show data of a requested book.

        Check if the book is listed in the database. If so, print
        out all its data.

        Parameters:
            titl - str containing a title of requested book
        """

        the_one = [b for b in self.books if b.title == titl]

        if not the_one:
            print("I don't know this book.")
            return False
        
        the_one = the_one[0]

        print(f"""{the_one.title} by {the_one.author}
        genre: {the_one.genre}
        added by {the_one.username}
        average rating: {the_one.rating[:-1]}
        see more: {the_one.link}""")

    def parse_rec(self, instream):
        """
        Find new book's data in the input string.

        Split string at '>' to find book's data. Expected markings:
        >t - title
        >a - author
        >g - genre
        Optional markings:
        >l - link (default: empty str)
        >r - rating (default: 5.0)
        Check input format. If correct, save data as a Book object
        and proceed to saving recommendation (function: save_rec).

        Parameters:
            instream - input str
        """

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
            rating = rating.strip()
            rating = float(rating)
        except AttributeError:
            rating = 5
        except ValueError:
            rating = 5

        if rating > 5 or rating < 0:
            print("Wrong rating!")
            return False

        a_book = Book(title, author, genre, link, self._name, rating)
        self.save_rec(a_book, self._rest)

    def parse_rate(self, instream):
        """
        Find rating data in the input string.

        Split string at '>' to find book's title and rating.
        Expected markings:
        >t - title
        >r - rating
        Check input format. If correct, save data as a Reader object
        and proceed to rating a book (function: rate_book).

        Parameters:
            instream - input str
        """

        title = None
        rating = None

        for ele in instream.split('>'):
            part = ele.split(' ', 1)[0]
            if part == "t":
                title = ele.split(' ', 1)[1]
            elif part == "r":
                rating = ele.split(' ', 1)[1]

        if title is None or rating is None:
            print("Wrong input format!")
            return False

        title = title.strip()
        try:
            rating = rating.strip()
            rating = float(rating)
        except ValueError:
            print("Wrong input format!")
            return False
        except AttributeError:
            rating = float(rating)

        if rating > 5 or rating < 0:
            print("Wrong rating!")
            return False


        a_read = Reader(title, self._name, rating)
        self.rate_book(a_read)

    def parse_text(self, instream):
        """
        Recognise user's command and proceed to a correct function.

        Split the instream at first " ", check if the first word
        is a command. Pass the remaining str to a new function.
        Possible commands:
        rec - recommend a new book, function: parse_rec (>save_rec>rates)
        rate - rate a known book, function: rate_book (>rates)
        getu - get recommendation based on a username, function: get_rec_user
        getg - get recommendation based on a genre, function: get_rec_genre
        info - get book's data, function: get_info

        Parameters:
            instream - input str
        """
        if len(instream.split(' ', 1)) == 2:
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
                print(genre)
                self.get_rec_genre(genre)

