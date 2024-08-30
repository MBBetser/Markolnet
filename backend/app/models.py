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
    phone_number = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(150), nullable=True)
    latitude = db.Column(db.Float, nullable=True)  # Latitude column
    longitude = db.Column(db.Float, nullable=True)  # Longitude column
    stores = relationship('Store', back_populates='owner')
    cart = db.relationship('Cart', uselist=False, back_populates='user')

    @property
    def is_active(self):
        return True
    

    def get_id(self):
        return str(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'user_type': self.user_type,
            'phone_number': self.phone_number,
        }
    

class Cart(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='cart')
    items = db.relationship('CartItem', back_populates='cart', cascade='all, delete-orphan')

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)  # Price at the time of adding to cart
    cart = db.relationship('Cart', back_populates='items')
    product = db.relationship('Product')
    
class Store(db.Model):
    __tablename__ = 'stores'
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, nullable=False)
    owner = relationship('User', back_populates='stores')
    products = relationship('StoreProduct', back_populates='store')

    def to_dict(self):
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'name': self.name,
            'products': [product.product.name for product in self.products],
        }
    

class Product(db.Model):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    image_path = Column(String)
    stores = relationship('StoreProduct', back_populates='product')
    cart_items = db.relationship('CartItem', back_populates='product')

    def getidbyname(self, name):
        return Product.query.filter_by(name=name).first().id
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'image_path': self.image_path
        }
    
    
class StoreProduct(db.Model):
    __tablename__ = 'store_products'
    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    quantity = Column(Integer, default=0)
    price = Column(Integer, default=0)
    
    store = relationship('Store', back_populates='products')
    product = relationship('Product', back_populates='stores')
