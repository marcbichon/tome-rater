import re

class User(object):
    """Keep track Tome Rater users and manage their ratings."""
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("{user_name}'s email has been successfully updated!".format(
        user_name=self.name))

    def __repr__(self):
        return "Name: {name}\nEmail: {email}\nBooks read: {number_of_books}\n".format(
        name=self.name, email=self.email, number_of_books=len(self.books))

    def __eq__(self, other_user):
        if self.name == other_user.name and self.email == other_user.email:
            return True
        else:
            return False

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        sum_of_ratings = 0
        number_of_ratings = 0
        for rating in self.books.values():
            if rating != None:
                number_of_ratings += 1
                sum_of_ratings += rating
        return sum_of_ratings / number_of_ratings

class Book(object):
    """Keep track Tome Rater catalog and manage the books ratings."""
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def _set_isbn(self, new_isbn):
        """Update ISBN of a given book.

        This method has been set private in order to ensure unique ISBNs and
        prevent hash issues in the TomeRater.books dict. It is called only by
        the 'set_isbn' method in the TomeRater class. The populate.py script
        will generate an error when trying to call novel1.set_isbn() method.
        It should be updated to call Tome_Rater.set_isbn() providing book
        and new ISBN.
        """
        self.isbn = new_isbn
        print("The ISBN of {book_title} has been successfully updated!".format(
        book_title=self.title))

    def add_rating(self, rating):
        if rating >= 0 and rating <= 4:
            self.ratings.append(rating)
        else:
            print("Invalid Rating")

    def __eq__(self, other_book):
        if self.title == other_book.title and self.isbn == other_book.isbn:
            return True
        else:
            return False

    def get_average_rating(self):
        sum_of_ratings = 0
        for rating in self.ratings:
            sum_of_ratings += rating
        return sum_of_ratings / len(self.ratings)

    def __hash__(self):
        return hash((self.title, self.isbn))

    def __repr__(self):
        return "{title}".format(title=self.title)

class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title=self.title, author=self.author)

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title=self.title,
        level=self.level, subject=self.subject)

class TomeRater(object):
    def __init__(self):
        self.users = {}
        self.books = {}

    def __eq__(self, other_tome_rater):
        if self.users == other_tome_rater.users and self.books == other_tome_rater.books:
            return True
        else:
            return False

    def create_book(self, title, isbn):
        if self.isbn_available(isbn):
            new_book = Book(title, isbn)
            self.books[new_book] = 0
            return new_book
        else:
            print("This isbn is already used by another book!")

    def create_novel(self, title, author, isbn):
        if self.isbn_available(isbn):
            new_fiction = Fiction(title, author, isbn)
            self.books[new_fiction] = 0
            return new_fiction
        else:
            print("This isbn is already used by another book!")

    def create_non_fiction(self, title, subject, level, isbn):
        if self.isbn_available(isbn):
            new_non_fiction = Non_Fiction(title, subject, level, isbn)
            self.books[new_non_fiction] = 0
            return new_non_fiction
        else:
            print("This isbn is already used by another book!")

    def isbn_available(self, isbn):
        isbn_is_available = True
        for book in self.books:
            if book.get_isbn() == isbn:
                isbn_is_available = False
                break
        return isbn_is_available

    def set_isbn(self, book, new_isbn):
        """Update ISBN of a given book.

        Update ISBNs for book objects and prevents the hash issues that occur
        if set_isbn() was called directly from the Book object. It calls the
        Book._set_isbn "semi-private" method.
        """
        read_count = self.books.pop(book)
        book._set_isbn(new_isbn)
        self.books[book] = read_count

    def add_book_to_user(self, book, email, rating=None):
        if email in self.users:
            user = self.users.get(email)
            user.read_book(book, rating)
            if rating != None:
                book.add_rating(rating)
            if book in self.books:
                self.books[book] += 1
            else:
                self.books[book] = 1
        else:
            print("No user with email {email}!".format(email=email))

    def add_user(self, name, email, user_books=None):
        if not re.match(r"[^@ ]+@[^@ ]+\.[^@]+", email):
            print("This is not a valid email!")
        elif email in self.users:
            print("A user with this email already exists!")
        else:
            new_user = User(name, email)
            self.users[email] = new_user
            if user_books != None:
                for book in user_books:
                    self.add_book_to_user(book, email)

    def print_catalog(self):
        print("\n############## Catalog ##############\n")
        for book in self.books:
            print("- {book}".format(book=book))
        print("\n#####################################\n")

    def print_users(self):
        print("\n############### Users ###############\n")
        for user in self.users.values():
            print(user)
        print("#####################################\n")

    def most_read_book(self):
        most_read_book = None
        most_read_value = 0
        for book, read_count in self.books.items():
            if read_count > most_read_value:
                most_read_book = book
                most_read_value = read_count
        return most_read_book

    def highest_rated_book(self):
        highest_rated_book = None
        highest_average_rating = 0
        for book in self.books:
            rating = book.get_average_rating()
            if rating > highest_average_rating:
                highest_rated_book = book
                highest_average_rating = rating
        return highest_rated_book

    def most_positive_user(self):
        most_positive_user = None
        highest_average_rating = 0
        for user in self.users.values():
            rating = user.get_average_rating()
            if rating > highest_average_rating:
                most_positive_user = user
                highest_average_rating = rating
        return most_positive_user

    def get_n_most_read_books(self, n):
        sorted_books = sorted(self.books, key=self.books.__getitem__, reverse=True)
        ranking = ""
        for i, book in enumerate(sorted_books[:n]):
            ranking += "{rank} - {book}\n".format(rank=i+1, book=book)
        return ranking

    def get_n_most_prolific_readers(self, n):
        readers = []
        for user in self.users.values():
            for i, reader in enumerate(readers):
                if len(user.books) > len(reader.books):
                    readers.insert(i, user)
                    break
            if user not in readers:
                readers.append(user)
        ranking = ""
        for i, reader in enumerate(readers[:n]):
            ranking += "{rank} -\n{reader}\n".format(rank=i+1, reader=reader)
        return ranking
