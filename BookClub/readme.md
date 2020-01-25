# BookClub Intern

#### Soon in your own book club Discord server!

BookClub Intern pomoże ci zarządzać biblioteką - doda na półki nowe
książki, zanotuje książki przeczytane przez poszczególnych członków
społeczności i zaproponuje nowe książki do przeczytania!

## Instalacja

BookClub Intern korzysta jedynie z bibliotek wbudowanych dla Pythona 3.7.
W celu instalacji należy pobrać repozytorium spod adresu:
> https://github.com/joasta/BookClub

## Uruchomienie

Plikiem, który uruchamia logikę programu, jest BookClub.py
w folderze BookClub.

## Opis działania

Program obsługuje dwie 'bazy danych' - listę poleconych książek (books.txt)
i listę ocen książek podawanych przez użytkowników (readers.txt).

Każda książka w bazie danych ma zapisane: tytuł, autora, gatunek, imię osoby
polecającej oraz średnią ocenę wszystkich użytkowników, którzy ją przeczytali.
Dodatkowo może być przechowywany link do strony internetowej z opisem książki.

Każda ocena w bazie danych przechowuje imię oceniającego, tytuł książki i
wystawioną ocenę.

Po uruchomieniu program pyta o imię użytkownika i łączy się z biblioteką
('bazami danych'). Program przyjmuje następnie jedną z sześciu komend:

* **q** - wychodzi z programu

* **rec** - zapisuje nową poleconą książkę w bibliotece i ocenę użytkownika na jego
	karcie bibliotecznej.

	Parametry obowiązkowe, w dowolnej kolejności:
	* _>t [title]_ - str, tytuł książki
	* _>a [author]_ - str, autor/autorzy książki
	* _>g [genre]_ - str, gatunek/gatunki książki
  
	Parametry opcjonalne, w dowolnej kolejności:
	* _>l [link]_ - str, link do strony z opisem książki (domyślnie: pusty)
    * _>r [rating]_ - float z zakresu <0, 5>, ocena książki (domyślnie: 5.0)

	Przykład użycia: __*rec >t Optics >a Eugene Hecht >g science >r 4.5*__

* **rate** - zapisuje nową ocenę znanej już książki (możliwa aktualizacja) i aktualizuje
	średnią ocenę według czytelników.

	Parametry obowiązkowe, w dowolnej kolejności:
	* _>t [title]_ - str, tytuł książki
    * _>r [rating]_ - float z zakresu <0, 5>, ocena książki

	Przykład użycia: __*rate >t Optics >r 4*__

* **getu** - podaje propozycję książki do przeczytania w oparciu o książki
	lubiane przez podanego użytkownika.

	Parametry obowiązkowe:
	* _[username]_ - str, imię użytkownika, z którego polubionych zostanie
    polecona książka

	Przykład użycia: __*getu Ginger*__

* **getg** - podaje propozycję książki do przeczytania w oparciu o wybrany gatunek.

	Parametry obowiązkowe:
	* _[genre]_ - str, gatunek, z którego zostanie polecona książka

	Przykład użycia: __*getu poetry*__

* **info** - podaje informacje na temat książki przechowywane w bibliotece.

	Parametry obowiązkowe:
	* _[title]_ - str, tytuł książki

	Przykład użycia: __*info Optics*__

## Autor

Joanna Starobrat, kontakt: joanna.starobrat@gmail.com