import pandas as pd
import re
from random import randint

def rates(title, name, rating, books):
    with open('BookClub\\reader.csv', 'rb') as f:
        readers = pd.read_csv(f, sep="|")

    duplicate = readers.loc[readers['title']==title]
    duplicate = duplicate.loc[readers['name']==name]
    if not duplicate.empty:
        readers.at[(readers['title']==title) & (readers['name']==name), 'rating'] = rating
    else:
        entry = pd.DataFrame([[readers.shape[0], title, name, rating]], columns = readers.columns)
        readers = readers.append(entry)
        
    with open('BookClub\\reader.csv', 'wb') as f:
        readers.to_csv("BookClub\\reader.csv", sep='|', index=False)

    list_ranks = readers.loc[readers['title']==title]
    list_ranks = list_ranks['rating'].to_list()
    list_ranks = [float(x) for x in list_ranks]
    average = sum(list_ranks) / len(list_ranks)
    books.at[books['title']==title, 'rating'] = average

    with open('BookClub\\book.csv', 'wb') as f:
        books.to_csv("BookClub\\book.csv", sep='|', index=False)

    return True

def print_rec(rec, name):
    with open('BookClub\\book.csv', 'r') as f:
        books = pd.read_csv(f, sep="|")

    try:
        regex = r'(?:\()([\w\W]+)(?:\))'
        title = re.search(regex, rec).group(1)
    except AttributeError:
        print("Wrong format! Try again.")
        return False
        
    try:
        regex = r'(?:<)([\d.,]+)(?:>)'
        rate = re.search(regex, rec).group(1)
        rec = rec.replace("<" + rate + ">","")
        rate = int(rate)
    except AttributeError:
        rate = 5
    except ValueError:
        rate = 5

    if title in books['title'].tolist():
        print("The book is already on the list! I'll add it to your library card.")
        rates(title, name, rate, books)
        return True

    try:
        regex = r'(?:\[)([\w\W]+)(?:\])'
        genre = re.search(regex, rec).group(1)
        regex = r'(?:\{)([\w\W]+)(?:\})'
        author = re.search(regex, rec).group(1)
    except AttributeError:
        print("Wrong format! Try again.")
        return False

    try:
        regex = r'(http[\S]+)'
        link = re.search(regex, rec).group(1)
        rec = rec.replace(link,"")
    except AttributeError:
        link = ""

    print(f"\nNew recommendation by {name}!\nGenre: {genre}\nTitle: {title}\nAuthor: {author}\nLink to description: {link}")
    rec = rec.replace("[" + genre + "]","")
    rec = rec.replace("{" + author + "}","")
    rec = rec.replace("(" + title + ")","")
    rec = rec.lstrip()
    rec = re.sub(' +', ' ', rec)
    print(rec + "\n")

    entry = pd.DataFrame([[books.shape[0], title, author, genre, link, name, rate]], columns = books.columns)
    books = books.append(entry)

    rates(title, name, rate, books)

    return 

def rate_book(rating, name):
    try:
        regex = r'(?:\()([\w\W]+)(?:\))'
        title = re.search(regex, rating).group(1)
    except AttributeError:
        print("Wrong format! Try again.")
        return False

    rating = rating.replace("(" + title + ")","")
    rating = rating.strip()
    rating = rating.strip("<")
    rating = rating.strip(">")
    try:
        rating = float(rating)
    except ValueError:
        print('Wrong format! Try again.')
        return False

    if rating > 5 and rating < 0:
        print("Wrong rating! Try again.")
        return False

    with open('BookClub\\book.csv', 'rb') as f:
        books = pd.read_csv(f, sep="|")

    if title not in books['title'].tolist():
        print("I don't know that book. Recommend it first!")
        return False

    else:
        rates(title, name, rating, books)

def get_rec_user(input, name):
    with open('BookClub\\reader.csv', 'rb') as f:
        readers = pd.read_csv(f, sep="|")
        
    input = input.strip()
    target_books = readers.loc[readers['name']==input]
    if target_books.empty:
        print("There's no library card under such a name.")
        return False

    target_books = target_books.loc[target_books['rating']>=2.5]
    if target_books.empty:
        print("I have no books to recommend.")
        return False
    
    read_books = readers.loc[readers['name']==name]
    read_books = read_books['title'].to_list()

    target_books = target_books['title'].to_list()

    recs = [i for i in target_books if i not in read_books]
    if recs == []:
        print("I have nothing to recommend.")
        return False

    recommended = recs[randint(0, len(recs)-1)]

    with open('BookClub\\book.csv', 'rb') as f:
        books = pd.read_csv(f, sep="|")
    
    the_one = books[books['title'] == recommended]
    print(f"My recommendation:\n{the_one.iloc[0]['title']} by {the_one.iloc[0]['author']} - added by {the_one.iloc[0]['name']}, average rating: {the_one.iloc[0]['rating']}")

def get_rec_genre(input, name):
    with open('BookClub\\reader.csv', 'rb') as f:
        readers = pd.read_csv(f, sep="|")
        
    with open('BookClub\\book.csv', 'rb') as f:
        books = pd.read_csv(f, sep="|")
        
    input = input.strip()

    genrelist = books['genre'].to_list()
    indices = [input in i for i in genrelist]
    target_books = books.loc[indices]
    if target_books.empty:
        print("That section of our library is yet empty.")
        return False
    
    read_books = readers.loc[readers['name']==name]
    read_books = read_books['title'].to_list()

    target_books = target_books['title'].to_list()

    recs = [i for i in target_books if i not in read_books]
    if recs == []:
        print("I have nothing to recommend.")
        return False

    recommended = recs[randint(0, len(recs)-1)]
    
    the_one = books[books['title'] == recommended]
    print(f"""My recommendation:\n{the_one.iloc[0]['title']} by {the_one.iloc[0]['author']}
    genre: {the_one.iloc[0]['genre']}
    added by {the_one.iloc[0]['name']}
    average rating: {the_one.iloc[0]['rating']}""")

def get_info(input):
    with open('BookClub\\book.csv', 'rb') as f:
        books = pd.read_csv(f, sep="|")
        
    input = input.strip()
    the_one = books[books['title']==input]

    if the_one.empty:
        print("I don't know this book.")
        return False

    print(f"""{the_one.iloc[0]['title']} by {the_one.iloc[0]['author']}
    genre: {the_one.iloc[0]['genre']}
    added by {the_one.iloc[0]['name']}
    average rating: {the_one.iloc[0]['rating']}
    see more: {the_one.iloc[0]['link']}""")

def parse_input(input, name):
    
    if input[0:3] == "rec":
        print_rec(input[4:], name)
        
    elif input[0:4] == "rate":
        rate_book(input[5:], name)

    elif input[0:4] == "getu":
        get_rec_user(input[5:], name)

    elif input[0:4] == "getg":
        get_rec_genre(input[5:], name)

    elif input[0:4] == "info":
        get_info(input[5:])
    else:
        pass

if __name__ is '__main__':
    #name = input("Who are you?\n")
    name="jj"
    proceed = True
    while proceed:
        instream = input("What do you want to do? rec/rate/info/getu/getg\n")
        if instream == "q":
            proceed = False
        elif instream == "":
            pass
        else:
            #parse_input("rate (Book) <4.5>", name)
            #parse_input("getu j", name)
            #parse_input("getg fiction", name)
            #parse_input("info Book5", name)
            parse_input("rec (Book7) {Anna} [poem] http://www.wp.pl wonderful book", name)
