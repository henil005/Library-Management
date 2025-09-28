# import datetime
# import os
# import re

# # File paths for storing data
# CUSTOMER_FILE = "customers.txt"
# BOOK_FILE = "books.txt"

# class Book:
#     def __init__(self, title, author, isbn, price):
#         self.title = title
#         self.author = author
#         self.isbn = isbn
#         self.price = price
#         self.checked_out = False
#         self.due_date = None
#         self.borrowed_by = None

#     def __str__(self):
#         status = "Available" if not self.checked_out else f"Checked Out (Due: {self.due_date})"
#         return f"{self.title} by {self.author} (ISBN: {self.isbn}, Price: ₹{self.price}) - {status}"


# class Customer:
#     def __init__(self, username, password):
#         self.username = username
#         self.password = password
#         self.borrowed_books = []
#         self.fine = 0.0

#     def __str__(self):
#         return f"Customer: {self.username}, Borrowed Books: {len(self.borrowed_books)}, Fine: ₹{self.fine:.2f}"


# class Library:
#     def __init__(self):
#         self.books = []
#         self.customers = []
#         self.admin_username = "admin"
#         self.admin_password = "admin123"
#         self.load_data()

#     def add_book(self, title, author, isbn, price):
#         if price < 10 or price > 100:
#             print("Price must be between ₹10 and ₹100.")
#             return
#         book = Book(title, author, isbn, price)
#         self.books.append(book)
#         print(f"Book '{title}' added to the library with price ₹{price}.")

#     def remove_book(self, isbn):
#         book = self.find_book_by_isbn(isbn)
#         if book:
#             self.books.remove(book)
#             print(f"Book '{book.title}' removed from the library.")
#         else:
#             print("Book not found.")

#     def view_books(self):
#         if not self.books:
#             print("No books available in the library.")
#         else:
#             print("Books in the library:")
#             for book in self.books:
#                 print(book)

#     def borrow_book(self, isbn, customer):
#         book = self.find_book_by_isbn(isbn)
#         if book:
#             if book.checked_out:
#                 print(f"Book '{book.title}' is already checked out.")
#             else:
#                 book.checked_out = True
#                 book.due_date = datetime.datetime.now() + datetime.timedelta(days=14)  # 14-day loan period
#                 book.borrowed_by = customer.username
#                 customer.borrowed_books.append(book)
#                 print(f"Book '{book.title}' borrowed by {customer.username}. Due date: {book.due_date}.")
#         else:
#             print("Book not found.")

#     def return_book(self, isbn, customer):
#         book = self.find_book_by_isbn(isbn)
#         if book:
#             if book.checked_out and book.borrowed_by == customer.username:
#                 book.checked_out = False
#                 days_late = (datetime.datetime.now() - book.due_date).days
#                 if days_late > 0:
#                     fine = days_late * (book.price * 0.1)  # 10% of book price per day
#                     customer.fine += fine
#                     print(f"Book '{book.title}' returned {days_late} days late. Fine: ₹{fine:.2f}.")
#                 else:
#                     print(f"Book '{book.title}' returned on time. No fine.")
#                 book.due_date = None
#                 book.borrowed_by = None
#                 customer.borrowed_books.remove(book)
#             else:
#                 print(f"Book '{book.title}' is not checked out by {customer.username}.")
#         else:
#             print("Book not found.")

#     def find_book_by_isbn(self, isbn):
#         for book in self.books:
#             if book.isbn == isbn:
#                 return book
#         return None

#     def register_customer(self, username, password):
#         if self.find_customer_by_username(username):
#             print("Username already exists. Please choose a different username.")
#         else:
#             if self.validate_password(password):
#                 customer = Customer(username, password)
#                 self.customers.append(customer)
#                 print(f"Customer '{username}' registered successfully.")
#             else:
#                 print("Password must be at least 8 characters long, contain at least one number, and one special character.")

#     def validate_password(self, password):
#         if len(password) < 8:
#             return False
#         if not re.search(r"\d", password):  # At least one number
#             return False
#         if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):  # At least one special character
#             return False
#         return True

#     def find_customer_by_username(self, username):
#         for customer in self.customers:
#             if customer.username == username:
#                 return customer
#         return None

#     def login_customer(self, username, password):
#         customer = self.find_customer_by_username(username)
#         if customer and customer.password == password:
#             return customer
#         return None

#     def login_admin(self, username, password):
#         return username == self.admin_username and password == self.admin_password

#     def view_customers(self):
#         if not self.customers:
#             print("No customers registered.")
#         else:
#             print("Registered customers:")
#             for customer in self.customers:
#                 print(customer)

#     def view_borrowed_books(self):
#         borrowed_books = [book for book in self.books if book.checked_out]
#         if borrowed_books:
#             print("Borrowed books:")
#             for book in borrowed_books:
#                 print(f"{book} (Borrowed by: {book.borrowed_by})")
#         else:
#             print("No books are currently borrowed.")

#     def save_data(self):
#         try:
#             with open(CUSTOMER_FILE, 'w') as cf:
#                 for customer in self.customers:
#                     cf.write(f"{customer.username},{customer.password}\n")
#             with open(BOOK_FILE, 'w') as bf:
#                 for book in self.books:
#                     bf.write(f"{book.title},{book.author},{book.isbn},{book.price},{book.checked_out},{book.due_date},{book.borrowed_by}\n")
#             print("Data saved successfully.")
#         except Exception as e:
#             print(f"Error saving data: {e}")

#     def load_data(self):
#         try:
#             if os.path.exists(CUSTOMER_FILE):
#                 with open(CUSTOMER_FILE, 'r') as cf:
#                     for line in cf:
#                         username, password = line.strip().split(',')
#                         self.customers.append(Customer(username, password))
#             if os.path.exists(BOOK_FILE):
#                 with open(BOOK_FILE, 'r') as bf:
#                     for line in bf:
#                         title, author, isbn, price, checked_out, due_date, borrowed_by = line.strip().split(',')
#                         book = Book(title, author, isbn, float(price))
#                         book.checked_out = checked_out == 'True'
#                         if due_date != 'None':
#                             book.due_date = datetime.datetime.strptime(due_date, '%Y-%m-%d %H:%M:%S.%f')
#                         book.borrowed_by = borrowed_by if borrowed_by != 'None' else None
#                         self.books.append(book)
#             print("Data loaded successfully.")
#         except Exception as e:
#             print(f"Error loading data: {e}")


# # Main Program
# def main():
#     library = Library()

#     while True:
#         print("\nLibrary Management System:")
#         print("1. Customer Login")
#         print("2. Customer Register")
#         print("3. Admin Login")
#         print("4. Exit")

#         choice = input("Enter your choice: ")

#         if choice == '1':
#             username = input("Enter username: ")
#             password = input("Enter password: ")
#             customer = library.login_customer(username, password)
#             if customer:
#                 customer_menu(library, customer)
#             else:
#                 print("Invalid username or password.")

#         elif choice == '2':
#             username = input("Enter username: ")
#             password = input("Enter password: ")
#             library.register_customer(username, password)

#         elif choice == '3':
#             username = input("Enter admin username: ")
#             password = input("Enter admin password: ")
#             if library.login_admin(username, password):
#                 admin_menu(library)
#             else:
#                 print("Invalid admin credentials.")

#         elif choice == '4':
#             library.save_data()
#             print("Exiting the system. Goodbye!")
#             break

#         else:
#             print("Invalid choice. Please try again.")


# def customer_menu(library, customer):
#     while True:
#         print(f"\nCustomer Menu: {customer.username}")
#         print("1. View all books")
#         print("2. Borrow a book")
#         print("3. Return a book")
#         print("4. View borrowed books")
#         print("5. Make Payment")
#         print("6. Logout")

#         choice = input("Enter your choice: ")

#         if choice == '1':
#             library.view_books()

#         elif choice == '2':
#             isbn = input("Enter book ISBN to borrow: ")
#             library.borrow_book(isbn, customer)

#         elif choice == '3':
#             isbn = input("Enter book ISBN to return: ")
#             library.return_book(isbn, customer)

#         elif choice == '4':
#             if customer.borrowed_books:
#                 print("Books borrowed by you:")
#                 for book in customer.borrowed_books:
#                     print(book)
#             else:
#                 print("You have not borrowed any books.")

#         elif choice == '5':
#             isbn = input("Enter book ISBN to make payment: ")
#             book = library.find_book_by_isbn(isbn)
#             if book:
#                 if book.checked_out and book.borrowed_by == customer.username:
#                     print(f"Payment for book '{book.title}' (Price: ₹{book.price})")
#                     print("Select payment method:")
#                     print("1. Direct Bank Account")
#                     print("2. UPI")
#                     print("3. Wallet")
#                     payment_method = input("Enter your choice: ")

#                     if payment_method == '1':
#                         account_number = input("Enter your bank account number: ")
#                         if len(account_number) == 12 and account_number.isdigit():
#                             print(f"Payment of ₹{book.price:.2f} successful from bank account {account_number}.")
#                         else:
#                             print("Invalid account number.")

#                     elif payment_method == '2':
#                         upi_id = input("Enter your UPI ID: ")
#                         if "@" in upi_id:
#                             print(f"Payment of ₹{book.price:.2f} successful using UPI ID {upi_id}.")
#                         else:
#                             print("Invalid UPI ID.")

#                     elif payment_method == '3':
#                         wallet_password = input("Enter your wallet password: ")
#                         if len(wallet_password) >= 8:
#                             print(f"Payment of ₹{book.price:.2f} successful using wallet.")
#                         else:
#                             print("Invalid wallet password.")

#                     else:
#                         print("Invalid payment method.")
#                 else:
#                     print(f"Book '{book.title}' is not checked out by you.")
#             else:
#                 print("Book not found.")

#         elif choice == '6':
#             print("Logging out.")
#             break

#         else:
#             print("Invalid choice. Please try again.")


# def admin_menu(library):
#     while True:
#         print("\nAdmin Menu:")
#         print("1. Add a book")
#         print("2. Remove a book")
#         print("3. View all books")
#         print("4. View all customers")
#         print("5. View borrowed books")
#         print("6. Logout")

#         choice = input("Enter your choice: ")

#         if choice == '1':
#             title = input("Enter book title: ")
#             author = input("Enter book author: ")
#             isbn = input("Enter book ISBN: ")
#             price = float(input("Enter book price (₹10 to ₹100): "))
#             library.add_book(title, author, isbn, price)

#         elif choice == '2':
#             isbn = input("Enter book ISBN to remove: ")
#             library.remove_book(isbn)

#         elif choice == '3':
#             library.view_books()

#         elif choice == '4':
#             library.view_customers()

#         elif choice == '5':
#             library.view_borrowed_books()

#         elif choice == '6':
#             print("Logging out.")
#             break

#         else:
#             print("Invalid choice. Please try again.")


# if __name__ == "__main__":
#     main()