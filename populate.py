from TomeRater import *

Tome_Rater = TomeRater()

#Create some books:
book1 = Tome_Rater.create_book("Society of Mind", 12345678)
novel1 = Tome_Rater.create_novel("Alice In Wonderland", "Lewis Carroll", 12345)
nonfiction1 = Tome_Rater.create_non_fiction("Automate the Boring Stuff", "Python", "beginner", 1929452)
nonfiction2 = Tome_Rater.create_non_fiction("Computing Machinery and Intelligence", "AI", "advanced", 11111938)
novel2 = Tome_Rater.create_novel("The Diamond Age", "Neal Stephenson", 10101010)
novel3 = Tome_Rater.create_novel("There Will Come Soft Rains", "Ray Bradbury", 10001000)

#Attempt to create book with already assigned ISBN:
print("-- Test: create book with ISBN already used by another book --")
novel3_duplicate = Tome_Rater.create_novel("There Will Come Soft Rains 2", "Ray Bradbury", 10001000)

#Update ISBN:
print("\n-- Test: update isbn --")
Tome_Rater.set_isbn(novel1, 9781536831139)

#Create users:
Tome_Rater.add_user("Alan Turing", "alan@turing.com")
Tome_Rater.add_user("David Marr", "david@computation.org")

#Attempt to create user with already used email:
print("\n-- Test: add user with email already used by another user --")
Tome_Rater.add_user("Fake David Marr", "david@computation.org")

#Attempt to create user with invalid email:
print("\n-- Test: add user with invalid email --")
Tome_Rater.add_user("Invalid Email", "invalid_email.com")

#Add a user with three books already read:
Tome_Rater.add_user("Marvin Minsky", "marvin@mit.edu", user_books=[book1, novel1, nonfiction1])

#Add books to a user one by one, with ratings:
Tome_Rater.add_book_to_user(book1, "alan@turing.com", 1)
Tome_Rater.add_book_to_user(novel1, "alan@turing.com", 3)
Tome_Rater.add_book_to_user(nonfiction1, "alan@turing.com", 3)
Tome_Rater.add_book_to_user(nonfiction2, "alan@turing.com", 4)
Tome_Rater.add_book_to_user(novel3, "alan@turing.com", 1)
Tome_Rater.add_book_to_user(novel2, "marvin@mit.edu", 2)
Tome_Rater.add_book_to_user(novel3, "marvin@mit.edu", 2)
Tome_Rater.add_book_to_user(novel3, "david@computation.org", 4)

#Print books catalog:
Tome_Rater.print_catalog()

#Print users:
Tome_Rater.print_users()

#Print most positive user:
print("\n-- Most positive user --\n")
print(Tome_Rater.most_positive_user())

#Print highest rated book:
print("\n-- Highest rated book --\n")
print(Tome_Rater.highest_rated_book())

#Print most read book:
print("\n-- Most read book --\n")
print(Tome_Rater.most_read_book())

#Print 5 most read books:
print("\n-- Ranking most read books --\n")
print(Tome_Rater.get_n_most_read_books(5))

#Print 2 most prolific readers:
print("\n-- Ranking most prolific readers --\n")
print(Tome_Rater.get_n_most_prolific_readers(2))
