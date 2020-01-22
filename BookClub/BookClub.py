import pandas as pd
import re

def print_rec(rec, name):
    books = ""

    with open('book.csv', 'rb') as f:
        books = pd.read_csv(f, sep="|")

    regex = r'(?:\()([\w\W]+)(?:\))'
    title = re.search(regex, rec).group(1)

    if title in books['title'].tolist():
        print("The book is already on the list! Consider marking it as read instead.")
        return False

    regex = r'(?:\[)([\w\W]+)(?:\])'
    genre = re.search(regex, rec).group(1)
    if genre is None:
        print("Wrong format! Try again.")
        return False
    regex = r'(?:\()([\w\W]+)(?:\))'
    author = re.search(regex, rec).group(1)
    if author is None:
        print("Wrong format! Try again.")
        return False
    regex = r'(http[\S]+)'
    link = re.search(regex, rec).group(1)
    if link is None:
        link = ""
    else:
        rec = rec.replace(link,"")
    #print(f"\nNew recommendation by {name}!\nGenre: {genre}\nTitle: {title}\nAuthor: {author}\nLink to description: {link}")
    rec = rec.replace("[" + genre + "]","")
    rec = rec.replace("{" + author + "}","")
    rec = rec.replace("(" + title + ")","")
    rec = rec.lstrip()
    rec = re.sub(' +', ' ', rec)
    print(rec + "\n")

    entry = pd.DataFrame([[books.shape[0], title, author, genre, link, name, 5]], columns = books.columns)
    books = books.append(entry)

    with open('book.csv', 'wb') as f:
        books.to_csv("book.csv", sep='|', index=False)

    return True

def rate_book(rating, name):
    books = ""
    readers = ""

    regex = r'(?:\()([\w\W]+)(?:\))'
    title = re.search(regex, rating).group(1)
    
    rating = rating.replace("(" + title + ")","")
    rating = rating.strip()
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
        with open('reader.csv', 'rb') as f:
            readers = pd.read_csv(f, sep="|")

        duplicate = readers.loc[readers['title']==title]
        duplicate = duplicate.loc[readers['name']==name]
        if duplicate is not None:
            readers.at[(readers['title']==title) & (readers['name']==name), 'rating'] = rating

        else:
            entry = pd.DataFrame([[readers.shape[0], title, name, rating]], columns = readers.columns)
            readers = readers.append(entry)
        
        with open('reader.csv', 'wb') as f:
            readers.to_csv("reader.csv", sep='|', index=False)

        list_ranks = readers.loc[readers['title']==title]
        list_ranks = list_ranks['rating'].to_list()
        list_ranks = [float(x) for x in list_ranks]
        average = sum(list_ranks) / len(list_ranks)
        books.at[books['title']==title, 'rating'] = average

        with open('book.csv', 'wb') as f:
            books.to_csv("book.csv", sep='|', index=False)

def get_rec(input, name):
    with open('BookClub\\reader.csv', 'rb') as f:
        readers = pd.read_csv(f, sep="|")
        
    input = input.lstrip()
    input = input.rstrip()
    print(input)
    target_books = readers.loc[readers['name']==input]
    if target_books is None:
        print("There's no library card under such a name.")
        return False

    target_books = target_books.loc[target_books['rating']>=2.5]
    if target_books is None:
        print("I have no books to recommend.")
        return False
    
    read_books = readers.loc[readers['name']==name]
    read_books = read_books['title'].to_list()
    print("Read:")
    print(read_books)

    target_books = target_books['title'].to_list()
    print("Other:")
    print(target_books)

    recs = [i for i in target_books if i not in read_books]
    print("Recs:")
    print(recs)


def parse_input(input, name):
    if input[0:3] == "rec":
        print_rec(input[3:], name)
        
    elif input[0:4] == "rate":
        rate_book(input[5:], name)

    if input[0:3] == "get":
        get_rec(input[3:], name)

    elif input[0:4] == "info":
        pass
    else:
        pass

if __name__ is '__main__':
    #name = input("Who are you?\n")
    name="k"
    proceed = True
    while proceed:
        instream = input("What do you want to do? rec/rate/info/get\n")
        if instream == "q":
            proceed = False
        else:
            #parse_input("rec bla bla [science-fiction] (Book) {Bill} https://www.onet.pl bla", name)
            #parse_input("rate (Book) 4", name)
            get_rec("get j", name)
