class Book:
    """Contains information about a single recommended book."""

    def __init__(self, title, author, genre, link, username, rating):
        self.title = title
        self.author = author
        self.genre = genre
        self.link = link
        self.username = username
        self.rating = rating

class Reader:
    """Contains rating of a single book by a specified user."""

    def __init__(self, title, username, rating):
        self.title = title
        self.username = username
        self.rating = rating