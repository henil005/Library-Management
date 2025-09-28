# import datetime
import os
import re
from datetime import datetime, timedelta  # Import both datetime and timedelta

# File path for storing data
CUSTOMER_FILE = "customers.txt"
BOOK_FILE = "books.txt"

class Book:
    def __init__(self, title, author, isbn, price):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.price = price
        self.checked_out = False
        self.due_date = None
        self.borrowed_by = None

    def __str__(self):
        status = "Available" if not self.checked_out else f"Checked Out (Due: {self.due_date})"
        return f"{self.title} by {self.author} (ISBN: {self.isbn}, Price: ₹{self.price}) - {status}"


class Customer:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.borrowed_books = []

    def __str__(self):
        return f"Customer: {self.username}, Borrowed Books: {len(self.borrowed_books)}"


class Library:
    def __init__(self):
        self.books = []
        self.customers = []
        self.admin_username = "admin"
        self.admin_password = "admin123"
        self.load_data()

    def add_book(self, title, author, isbn, price):
        if price < 10 or price > 100:
            print("Price must be between ₹10 and ₹100.")
            return
        book = Book(title, author, isbn, price)
        self.books.append(book)
        print(f"Book '{title}' added to the library with price ₹{price}.")

    def remove_book(self, isbn):
        book = self.find_book_by_isbn(isbn)
        if book:
            self.books.remove(book)
            print(f"Book '{book.title}' removed from the library.")
        else:
            print("Book not found.")

    def view_books(self):
        if not self.books:
            print("No books available in the library.")
        else:
            print("Books in the library:")
            for book in self.books:
                print(book)

    def borrow_book(self, isbn, customer):
        book = self.find_book_by_isbn(isbn)
        if book:
            if book.checked_out:
                print(f"Book '{book.title}' is already checked out.")
            else:
                print(f"Book '{book.title}' is available for borrowing.")
                
                # Ask the user to choose a payment method
                print(f"Book price: ₹{book.price}")
                print("Please select a payment method:")
                print("1. Credit Card")
                print("2. Debit Card")
                print("3. PayPal")
                payment_choice = input("Enter your choice (1/2/3): ")

                if payment_choice == '1':
                    payment_method = "Credit Card"
                elif payment_choice == '2':
                    payment_method = "Debit Card"
                elif payment_choice == '3':
                    payment_method = "PayPal"
                else:
                    print("Invalid choice. Cancelling borrow process.")
                    return

                # Process the payment
                payment = Payment(book.price)
                if payment.process_payment(payment_method):
                    # Proceed with borrowing the book
                    book.checked_out = True
                    book.due_date = datetime.now() + timedelta(days=14)  # 14-day loan period
                    # book.due_date = datetime.now() + datetime.timedelta(days=14)  # 14-day loan period
                    book.borrowed_by = customer.username
                    customer.borrowed_books.append(book)
                    print(f"Book '{book.title}' borrowed by {customer.username}. Due date: {book.due_date}.")
                else:
                    print("Payment failed. Unable to borrow the book.")
        else:
            print("Book not found.")

    def return_book(self, isbn, customer):
        book = self.find_book_by_isbn(isbn)
        if book:
            if book.checked_out and book.borrowed_by == customer.username:
                book.checked_out = False
                book.due_date = None
                book.borrowed_by = None
                customer.borrowed_books.remove(book)
                print(f"Book '{book.title}' returned successfully.")
            else:
                print(f"Book '{book.title}' is not checked out by {customer.username}.")
        else:
            print("Book not found.")

    def find_book_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def register_customer(self, username, password):
        if self.find_customer_by_username(username):
            print("Username already exists. Please choose a different username.")
        else:
            if self.validate_password(password):
                customer = Customer(username, password)
                self.customers.append(customer)
                print(f"Customer '{username}' registered successfully.")
            else:
                print("Password must be at least 8 characters long, contain at least one number, and one special character.")

    def validate_password(self, password):
        if len(password) < 8:
            return False
        if not re.search(r"\d", password):  # At least one number
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):  # At least one special character
            return False
        return True

    def find_customer_by_username(self, username):
        for customer in self.customers:
            if customer.username == username:
                return customer
        return None

    def login_customer(self, username, password):
        customer = self.find_customer_by_username(username)
        if customer and customer.password == password:
            return customer
        return None

    def login_admin(self, username, password):
        return username == self.admin_username and password == self.admin_password

    def view_customers(self):
        if not self.customers:
            print("No customers registered.")
        else:
            print("Registered customers:")
            for customer in self.customers:
                print(customer)

    def view_borrowed_books(self):
        borrowed_books = [book for book in self.books if book.checked_out]
        if borrowed_books:
            print("Borrowed books:")
            for book in borrowed_books:
                print(f"{book} (Borrowed by: {book.borrowed_by})")
        else:
            print("No books are currently borrowed.")

    def save_data(self):
        try:
            with open(CUSTOMER_FILE, 'w') as cf:
                for customer in self.customers:
                    cf.write(f"{customer.username},{customer.password}\n")
            with open(BOOK_FILE, 'w') as bf:
                for book in self.books:
                    due_date = book.due_date.strftime('%Y-%m-%d %H:%M:%S.%f') if book.due_date else 'None'
                    bf.write(f"{book.title},{book.author},{book.isbn},{book.price},{book.checked_out},{due_date},{book.borrowed_by}\n")
            print("Data saved successfully.")
        except Exception as e:
            print(f"Error saving data: {e}")

    def load_data(self):
        try:
            if os.path.exists(CUSTOMER_FILE):
                with open(CUSTOMER_FILE, 'r') as cf:
                    for line in cf:
                        username, password = line.strip().split(',')
                        self.customers.append(Customer(username, password))
            if os.path.exists(BOOK_FILE):
                with open(BOOK_FILE, 'r') as bf:
                    for line in bf:
                        title, author, isbn, price, checked_out, due_date, borrowed_by = line.strip().split(',')
                        book = Book(title, author, isbn, float(price))
                        book.checked_out = checked_out == 'True'
                        if due_date != 'None':
                            try:
                                book.due_date = datetime.strptime(due_date, '%Y-%m-%d %H:%M:%S.%f')
                            except ValueError:
                                book.due_date = None  # Handle incorrect date format
                        book.borrowed_by = borrowed_by if borrowed_by != 'None' else None
                        self.books.append(book)
            print("Data loaded successfully.")
        except Exception as e:
            print(f"Error loading data: {e}")

class Payment:
    def __init__(self, amount):
        self.amount = amount

    def process_payment(self, method):
        if method == "Credit Card":
            return self.process_credit_card()
        elif method == "Debit Card":
            return self.process_debit_card()
        elif method == "PayPal":
            return self.process_paypal()
        else:
            print("Invalid payment method.")
            return False
        
    def process_credit_card(self):
        print("Please enter your credit card details:")
        card_number = input("Card Number (XXXX-XXXX-XXXX-XXXX): ")
        # Validate card number format
        # if not re.match(r"\d{4}-\d{4}-\d{4}-\d{4}", card_number):
        #     print("Invalid card number format. Please enter the number as XXXX-XXXX-XXXX-XXXX.")
        #     return False
        
        cardholder_name = input("Cardholder Name: ")
        expiration_date = input("Expiration Date (MM/YY): ")
        # Validate expiration date format
        # if not re.match(r"\d{2}/\d{2}", expiration_date):
        #     print("Invalid expiration date format. Please enter it as MM/YY.")
        #     return False
        print("card_number is : "+card_number)
        print("cardholder_name : "+cardholder_name)
        print("expiration_date : "+expiration_date)
        print("\nPayment Successfully!")
        return True

    def process_debit_card(self):
        print("Please enter your debit card details:")
        card_number = input("Card Number (XXXX-XXXX-XXXX-XXXX): ")
        # Validate card number format
        # if not re.match(r"\d{4}-\d{4}-\d{4}-\d{4}", card_number):
        #     print("Invalid card number format. Please enter the number as XXXX-XXXX-XXXX-XXXX.")
        #     return False
        cardholder_name = input("Cardholder Name: ")
        expiration_month = input("Expiration Month (MM): ")
        expiration_year = input("Expiration Year (YYYY): ")
        # Validate expiration month and year format
        # if not re.match(r"\d{2}", expiration_month) or not re.match(r"\d{4}", expiration_year):
        #     print("Invalid expiration date format. Please enter the month as MM and year as YYYY.")
        #     return False
        print("card_number is : "+card_number)
        print("cardholder_name : "+cardholder_name)
        print("expiration MM/YYYY : "+expiration_month+"/"+expiration_year)
        print("\nPayment Successfully!")
        return True

    def process_paypal(self):
        print("Welcome to PayPal Payment System")
        # User inputs
        amount = float(input("Enter the amount to be paid (e.g., 10.00): "))
        currency = input("Enter the currency (e.g., USD): ").upper()
        # Simulate processing the payment (printing the entered details)
        print("\nProcessing your payment...")
        print(f"Amount: {amount} {currency}")
        print(f"Payment Method: PayPal")
        print(f"Payment Status: Approved (Simulated)")
        # Simulated confirmation
        print("\nPayment successfully processed!")
        print(f"Amount charged: {amount} {currency}")
        print("Thank you for using PayPal!")
        print("payment successfully...")
        return True

class LibrarySystem:
    def __init__(self):
        self.library = Library()

    def run(self):
        while True:
            print("\nLibrary Management System:")
            print("1. Customer Login")
            print("2. Customer Register")
            print("3. Admin Login")
            print("4. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                username = input("Enter username: ")
                password = input("Enter password: ")
                customer = self.library.login_customer(username, password)
                if customer:
                    self.customer_menu(customer)
                else:
                    print("Invalid username or password.")

            elif choice == '2':
                username = input("Enter username: ")
                password = input("Enter password: ")
                self.library.register_customer(username, password)

            elif choice == '3':
                username = input("Enter admin username: ")
                password = input("Enter admin password: ")
                if self.library.login_admin(username, password):
                    self.admin_menu()
                else:
                    print("Invalid admin credentials.")

            elif choice == '4':
                self.library.save_data()
                print("Exiting the system. Goodbye!")
                break

            else:
                print("Invalid choice. Please try again.")

    def customer_menu(self, customer):
        while True:
            print(f"\nCustomer Menu: {customer.username}")
            print("1. View all books")
            print("2. Borrow a book")
            print("3. Return a book")
            print("4. View borrowed books")
            print("5. Logout")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.library.view_books()

            elif choice == '2':
                isbn = input("Enter book ISBN to borrow: ")
                self.library.borrow_book(isbn, customer)

            elif choice == '3':
                isbn = input("Enter book ISBN to return: ")
                self.library.return_book(isbn, customer)

            elif choice == '4':
                if customer.borrowed_books:
                    print("Books borrowed by you:")
                    for book in customer.borrowed_books:
                        print(book)
                else:
                    print("You have not borrowed any books.")

            elif choice == '5':
                print("Logging out.")
                break

            else:
                print("Invalid choice. Please try again.")

    def admin_menu(self):
        while True:
            print("\nAdmin Menu:")
            print("1. Add a book")
            print("2. Remove a book")
            print("3. View all books")
            print("4. View all customers")
            print("5. View borrowed books")
            print("6. Logout")

            choice = input("Enter your choice: ")

            if choice == '1':
                title = input("Enter book title: ")
                author = input("Enter book author: ")
                isbn = input("Enter book ISBN: ")
                price = float(input("Enter book price (₹10 to ₹100): "))
                self.library.add_book(title, author, isbn, price)

            elif choice == '2':
                isbn = input("Enter book ISBN to remove: ")
                self.library.remove_book(isbn)

            elif choice == '3':
                self.library.view_books()

            elif choice == '4':
                self.library.view_customers()

            elif choice == '5':
                self.library.view_borrowed_books()

            elif choice == '6':
                print("Logging out.")
                break
            else:
                print("Invalid choice. Please try again.")
# create an instance of the LibrarySystem class and run the program
library_system = LibrarySystem()
library_system.run()
