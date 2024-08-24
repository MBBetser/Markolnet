from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from ..db import db
from ..models import Product
product_routes = Blueprint('product_routes', __name__,url_prefix='/products')

@product_routes.route('/')
def test():
    return 'Hey from products route!'

@product_routes.route('/add-product-to-db', methods=['POST'])
def create_product():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    product = Product(name=name, price=price)
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict())

@product_routes.route('/all')
def all_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])