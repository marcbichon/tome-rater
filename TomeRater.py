import re

class User(object):
    """Keep track of Tome Rater users.

    Attributes:
        name (str): The name of the user.
        email (str): The email of the user.
        books (dict): Books read by a user, keys are Books, values are
        ratings (int).

    """

    def __init__(self, name, email):
        """Constructor of User class.

        Args:
            name (str): The name of the user.
            email (str): The email of the user.

        """
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        """Return the user's email."""

        return self.email

    def change_email(self, address):
        """Update the user's email."""

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
        """Add a book to the user's books list.

        Args:
            book (Book): The book read by the user.
            rating (int, optional): The rating given by the user to this book.
            Defaults to None.

        Returns:
            None

        """

        self.books[book] = rating

    def get_average_rating(self):
        """Calculate the average of all ratings from the user and return it.

        Note
            This method does not use len() to calculate the number of ratings
            as we want to exclude ratings equal to None.

        """

        sum_of_ratings = 0
        number_of_ratings = 0
        for rating in self.books.values():
            if rating != None:
                number_of_ratings += 1
                sum_of_ratings += rating
        return sum_of_ratings / number_of_ratings

class Book(object):
    """Keep track of Tome Rater catalog and manage the books ratings.

    Attributes:
        title (string): The title of the book.
        isbn (string): The ISBN of the book.
        ratings (list): A list of all book's ratings.

    """

    def __init__(self, title, isbn):
        """Constructor of Book class.

        Args:
            title (str): The title of the book.
            isbn (int): The ISBN of the book.
        """

        self.title = title
        self.isbn = isbn
        self.ratings = []

    def get_title(self):
        """Return the book's title."""

        return self.title

    def get_isbn(self):
        """Return the book's ISBN."""

        return self.isbn

    def _set_isbn(self, new_isbn):
        """Update ISBN of a given book.

        Note:
            This method has been set private in order to ensure unique ISBNs
            and prevent hash issues in the TomeRater.books dict. It is called
            only by the 'set_isbn' method in the TomeRater class.

        Args:
            new_isbn (int): The new ISBN that will replace the previous
            attribute value.

        Returns:
            None

        """

        self.isbn = new_isbn
        print("The ISBN of {book_title} has been successfully updated!".format(
        book_title=self.title))

    def add_rating(self, rating):
        """Add a rating to the book object.

        Note:
            The rating should be included between 0 and 4. Otherwise it will
            print an error statement and the rating will not be added.

        Args:
            rating (int): The rating to be added.

        Returns:
            None

        """

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
        """Calculate the average of all the book's ratings and return it."""

        sum_of_ratings = 0
        for rating in self.ratings:
            sum_of_ratings += rating
        return sum_of_ratings / len(self.ratings)

    def __hash__(self):
        return hash((self.title, self.isbn))

    def __repr__(self):
        return "{title}".format(title=self.title)

class Fiction(Book):
    """Keep track of Tome Rater catalog's novels.

    This class inherits from the Book class. The main difference comes from
    the author attribute that is not existing in the Book class.

    Attributes:
        title (str): The title of the novel.
        author (str): The author of the novel.
        isbn (int): The ISBN of the novel.

    """

    def __init__(self, title, author, isbn):
        """Constructor of Fiction class.

        Note:
            It uses the constructor of the Book class then declares the author
            attribute.

        Args:
            title (str): The title of the book.
            author (str): The author of the novel.
            isbn (int): The ISBN of the book.
        """

        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        """Return the novel's author."""

        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title=self.title, author=self.author)

class NonFiction(Book):
    """Keep track of Tome Rater catalog's non fictions.

    This class inherits from the Book class. The main difference comes from
    the subject and level attributes that are not existing in the Book class.

    Attributes:
        title (str): The title of the book.
        subject (str): The subject of the book.
        level (str): The difficulty level of the book.
        isbn (int): The ISBN of the novel.

    """

    def __init__(self, title, subject, level, isbn):
        """Constructor of NonFiction class.

        Note:
            It uses the constructor of the Book class then declares the subject
            and level attributes.

        Args:
            title (str): The title of the book.
            subject (str): The subject of the book.
            level (str): The difficulty level of the book.
            isbn (int): The ISBN of the book.
        """

        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        """Return the book's subject."""

        return self.subject

    def get_level(self):
        """Return the book's level."""

        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title=self.title,
        level=self.level, subject=self.subject)

class TomeRater(object):
    """Manage a books catalog and the corresponding ratings given by users.

    This class allows to create new books or new users, manages the ratings
    given by users and gives some interesting analytics.

    Attributes:
        users (dict): Keys are emails (str), values are users (User).
        books (dict): Keys are books (Book), values are read counts (int).

    """

    def __init__(self):
        """Constructor of TomeRater class."""
        self.users = {}
        self.books = {}

    def __eq__(self, other_tome_rater):
        if self.users == other_tome_rater.users and self.books == other_tome_rater.books:
            return True
        else:
            return False

    def create_book(self, title, isbn):
        """Create a book, add it to the catalog and return it.

        Note:
            ISBNs should be unic in the catalog. This method first checks if
            the argument isbn is already used by another book from the catalog
            and prints an error if that is the case.

        Args:
            title (str): The title of the book.
            isbn (int): The ISBN of the book.

        Returns:
            The new Book object if the ISBN was available, None otherwise.

        """

        if self.isbn_available(isbn):
            new_book = Book(title, isbn)
            self.books[new_book] = 0
            return new_book
        else:
            print("This ISBN is already used by another book!")

    def create_novel(self, title, author, isbn):
        """Create a novel, add it to the catalog and return it.

        Note:
            ISBNs should be unic in the catalog. This method first checks if
            the argument isbn is already used by another book from the catalog
            and prints an error if that is the case.

        Args:
            title (str): The title of the novel.
            author (str): The author of the novel.
            isbn (int): The ISBN of the novel.

        Returns:
            The new Fiction object if the ISBN was available, None otherwise.

        """

        if self.isbn_available(isbn):
            new_fiction = Fiction(title, author, isbn)
            self.books[new_fiction] = 0
            return new_fiction
        else:
            print("This ISBN is already used by another book!")

    def create_non_fiction(self, title, subject, level, isbn):
        """Create a non fiction book, add it to the catalog and return it.

        Note:
            ISBNs should be unic in the catalog. This method first checks if
            the argument isbn is already used by another book from the catalog
            and prints an error if that is the case.

        Args:
            title (str): The title of the book.
            subject (str): The subject of the book.
            level (str): The difficulty level of the book.
            isbn (int): The ISBN of the novel.

        Returns:
            The new NonFiction object if the ISBN was available, None otherwise.

        """

        if self.isbn_available(isbn):
            new_non_fiction = NonFiction(title, subject, level, isbn)
            self.books[new_non_fiction] = 0
            return new_non_fiction
        else:
            print("This ISBN is already used by another book!")

    def isbn_available(self, isbn):
        """Check if the ISBN is available in the catalog.

        Args:
            isbn (str): The ISBN to be checked for availability.

        Returns:
            True if no book from the catalog uses this ISBN, False otherwise.

        """

        isbn_is_available = True
        for book in self.books:
            if book.get_isbn() == isbn:
                isbn_is_available = False
                break
        return isbn_is_available

    def set_isbn(self, book, new_isbn):
        """Update ISBN of a given book.

        Notes:
            Prevents the hash issues that occur if set_isbn() was called
            directly from the Book object. It uses the Book._set_isbn
            private method.

            ISBNs should be unic in the catalog. This method first checks if
            the argument new_isbn is already used by another book from the
            catalog and prints an error if that is the case.

        Args:
            book (Book): The book whose ISBN should be updated.
            new_isbn (int): The new ISBN that will replace the previous
            attribute value.

        Returns:
            None

        """

        if self.isbn_available(new_isbn):
            read_count = self.books.pop(book)
            book._set_isbn(new_isbn)
            self.books[book] = read_count
        else:
            print("This ISBN is already used by another book!")

    def add_book_to_user(self, book, email, rating=None):
        """Add a new book to the list of books read by an user.

        Notes:
            It first checks if a user with the given email exist. Otherwise, it
            prints an error message.

            This method uses the User.read_books method to add the book to the
            list of read books. Additionnaly, the book is either added to the
            catalog if not already there, or its read count is incremented to
            reflect this new reading.

        Args:
            book (Book): The book read by the user.
            email (str): The email of the user.
            rating (int, optional): The rating from the user on this book.
            Defaults to None.

        Returns:
            None

        """

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
        """Add a new user to the list of readers.

        Notes:
            It first checks if the given email is valid and that no reader with
            the given email already exist. Otherwise, it prints an error message
            in both cases.

            If a lits of books already read by this user is provided, they are
            added using the add_book_to_user method.

        Args:
            name (str): The name of the user.
            email (str): The email of the user.
            user_books (list, optional): The list of books already read by the
            user. Defaults to None.

        Returns:
            None

        """

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
        """Print all books from the catalog in a clear way."""

        print("\n-- Catalog --\n")
        for book in self.books:
            print("- {book}".format(book=book))

    def print_users(self):
        """Print all readers in a clear way."""

        print("\n-- Users --\n")
        for user in self.users.values():
            print(user)

    def most_read_book(self):
        """Search for the most read book and return it."""

        most_read_book = None
        most_read_value = 0
        for book, read_count in self.books.items():
            if read_count > most_read_value:
                most_read_book = book
                most_read_value = read_count
        return most_read_book

    def highest_rated_book(self):
        """Search for the highest rated book and return it."""

        highest_rated_book = None
        highest_average_rating = 0
        for book in self.books:
            rating = book.get_average_rating()
            if rating > highest_average_rating:
                highest_rated_book = book
                highest_average_rating = rating
        return highest_rated_book

    def most_positive_user(self):
        """Search for the most positive user and return it."""

        most_positive_user = None
        highest_average_rating = 0
        for user in self.users.values():
            rating = user.get_average_rating()
            if rating > highest_average_rating:
                most_positive_user = user
                highest_average_rating = rating
        return most_positive_user

    def get_n_most_read_books(self, n):
        """Search for the n most read books and return a ranking of these books.

        Args:
            n (int): The number of books to include in the ranking.

        Returns:
            A clear string representation of the ranking.

        """

        sorted_books = sorted(self.books, key=self.books.__getitem__, reverse=True)
        ranking = ""
        for i, book in enumerate(sorted_books[:n]):
            ranking += "{rank} - {book}\n".format(rank=i+1, book=book)
        return ranking

    def get_n_most_prolific_readers(self, n):
        """Search for the n most prolific readers and return a ranking of these
        readers.

        Args:
            n (int): The number of readers to include in the ranking.

        Returns:
            A clear string representation of the ranking.

        """

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
