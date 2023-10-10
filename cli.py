#!/usr/bin/python3

import click
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from main import UserType, User, Book, Order, OrderItem, Base  # Import OrderItem heree

# Create an SQLite database and session
engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

@click.group()
def cli():
    pass

@cli.command()
def add_book():
    title = input('Enter book title: ')
    price = float(input('Enter book price: '))
    book = Book(title=title, price=price)
    session.add(book)
    session.commit()
    print(f"Book added with ID {book.id}")


@cli.command()
def add_user():
    username = input('Enter username: ')
    user = User(username=username, user_type=UserType.CUSTOMER.value)
    session.add(user)
    session.commit()
    print(f"User added with ID {user.id}")

@cli.command()
def add_order():
    user_id = int(input("Enter user ID for the order: "))
    book_id = int(input("Enter book ID for the order: "))
    quantity = int(input("Enter quantity: "))

    user = session.query(User).filter_by(id=user_id).first()
    book = session.query(Book).filter_by(id=book_id).first()

    if user and book:
        order = Order(customer=user)
        order_item = OrderItem(order=order, book=book, quantity=quantity)
        session.add(order)
        session.add(order_item)
        session.commit()
        print(f"Order added with ID {order.id}")
    else:
        print("User or book not found. Please check the IDs.")

@cli.command()
def add_order_item():
    order_id = int(input("Enter order ID for the order item: "))
    book_id = int(input("Enter book ID for the order item: "))
    quantity = int(input("Enter quantity: "))

    order = session.query(Order).filter_by(id=order_id).first()
    book = session.query(Book).filter_by(id=book_id).first()

    if order and book:
        order_item = OrderItem(order=order, book=book, quantity=quantity)
        session.add(order_item)
        session.commit()
        print(f"Order item added with ID {order_item.id}")
    else:
        print("Order or book not found. Please check the IDs.")

# Define the search-books command
@cli.command()
def search_books():
    title_query = input("Enter a book title to search for: ")
    books = session.query(Book).filter(Book.title.ilike(f"%{title_query}%")).all()
    
    if books:
        print("Matching books:")
        for book in books:
            print(f"Book ID: {book.id}, Title: {book.title}, Price: ${book.price}")
    else:
        print("No matching books found.")

@cli.command()
def delete_user():
    user_id = int(input("Enter the ID of the user to delete: "))
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        session.delete(user)
        session.commit()
        print(f"User with ID {user_id} deleted successfully.")
    else:
        print(f"User with ID {user_id} not found.")
    

@cli.command()
def delete_order():
    order_id = int(input("Enter the ID of the order to delete: "))
    order = session.query(Order).filter_by(id=order_id).first()
    if order:
        session.delete(order)
        session.commit()
        print(f"Order with ID {order_id} deleted successfully.")
    else:
        print(f"Order with ID {order_id} not found.")


@cli.command()
def delete_order():
    order_id = int(input("Enter the ID of the order to delete: "))
    order = session.query(Order).filter_by(id=order_id).first()
    if order:
        session.delete(order)
        session.commit()
        print(f"Order with ID {order_id} deleted successfully.")
    else:
        print(f"Order with ID {order_id} not found.")

@cli.command()
def delete_order_item():
    order_item_id = int(input("Enter the ID of the order item to delete: "))
    order_item = session.query(OrderItem).filter_by(id=order_item_id).first()
    if order_item:
        session.delete(order_item)
        session.commit()
        print(f"Order item with ID {order_item_id} deleted successfully.")
    else:
        print(f"Order item with ID {order_item_id} not found.")




if __name__ == '__main__':
    cli()
