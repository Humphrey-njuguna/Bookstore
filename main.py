#!/usr/bin/python3

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum

# Create a SQLite database in memory for this example
engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class UserType(Enum):
    CUSTOMER = 'Customer'
    ADMINISTRATOR = 'Administrator'

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    user_type = Column(String, nullable=False)

    orders = relationship('Order', back_populates='customer')

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    customer = relationship('User', back_populates='orders')
    order_items = relationship('OrderItem', back_populates='order')

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship('Order', back_populates='order_items')
    book = relationship('Book')  # Add this line to specify the book relationship

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    user1 = User(username='customer1', user_type=UserType.CUSTOMER.value)
    user2 = User(username='admin', user_type=UserType.ADMINISTRATOR.value)
    session.add(user1)
    session.add(user2)

    book1 = Book(title='Book 1', price=19.99)
    book2 = Book(title='Book 2', price=29.99)
    session.add(book1)
    session.add(book2)

    order1 = Order(customer=user1)
    order2 = Order(customer=user2)
    session.add(order1)
    session.add(order2)

    # Create order items using book objects
    order_item1 = OrderItem(order=order1, book=book1, quantity=2)
    order_item2 = OrderItem(order=order2, book=book2, quantity=1)
    session.add(order_item1)
    session.add(order_item2)

    session.commit()

    customer_orders = session.query(Order).filter_by(customer=user1).all()
    for order in customer_orders:
        print(f"Order ID: {order.id}, Customer: {order.customer.username}")
        for item in order.order_items:
            print(f" - Book: {item.book.title}, Quantity: {item.quantity}")
