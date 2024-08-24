from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from .db import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    user_type = db.Column(db.String(50), nullable=False)
    stores = relationship('Store', back_populates='owner')
    sent_messages = relationship('Message', foreign_keys='Message.sender_id', back_populates='sender')
    received_messages = relationship('Message', foreign_keys='Message.receiver_id', back_populates='receiver')
    orders = relationship('Order', foreign_keys='Order.customer_id', back_populates='customer')

    @property
    def is_active(self):
        return True
        
    def get_id(self):
        return str(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'user_type': self.user_type
        }
    
class Store(db.Model):
    __tablename__ = 'stores'
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, nullable=False)
    owner = relationship('User', back_populates='stores')
    products = relationship('StoreProduct', back_populates='store')
    orders = relationship('Order', foreign_keys='Order.store_id', back_populates='store')

    def to_dict(self):
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'name': self.name,
            'products': [product.product.name for product in self.products],
            'orders' : [order.id for order in self.orders]
        }

class Product(db.Model):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Integer)
    stores = relationship('StoreProduct', back_populates='product')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price
        }
    
    
class StoreProduct(db.Model):
    __tablename__ = 'store_products'
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    quantity = Column(Integer, default=0)
    
    store = relationship('Store', back_populates='products')
    product = relationship('Product', back_populates='stores')

class Order(db.Model):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('users.id'))
    store_id = Column(Integer, ForeignKey('stores.id'))
    customer = relationship('User', back_populates='orders')
    store = relationship('Store', back_populates='orders')
    items = relationship('OrderItem', back_populates='order')

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer)
    quantity = Column(Integer)
    order = relationship('Order', back_populates='items')

class Message(db.Model):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, ForeignKey('users.id'))
    receiver_id = Column(Integer, ForeignKey('users.id'))
    content = Column(Text, nullable=False)
    sender = relationship('User', foreign_keys=[sender_id], back_populates='sent_messages')
    receiver = relationship('User', foreign_keys=[receiver_id], back_populates='received_messages')
