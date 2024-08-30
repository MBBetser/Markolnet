from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from ..db import db
from ..models import Product, StoreProduct, Order
product_routes = Blueprint('product_routes', __name__,url_prefix='/products')

@product_routes.route('/')
def test():
    return 'Hey from products route!'

@product_routes.route('/add-product-to-db', methods=['POST'])
def create_product():
    data = request.get_json()
    name = data.get('name')
    filename = data.get('filename')
    print(filename) 
    image_path = f'assets/{filename}'

    product = Product(name=name, image_path=image_path)
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict())

@product_routes.route('/order', methods=['POST'])
def create_order():
    data = request.get_json()
    store_id = data.get('store_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    store_product = StoreProduct.query.filter_by(store_id=store_id, product_id=product_id).first()
    if not store_product or store_product.quantity < quantity:
        return jsonify({'error': 'Not enough stock'}), 400

    total_price = store_product.price * quantity
    order = Order(store_id=store_id, product_id=product_id, quantity=quantity, total_price=total_price)

    store_product.quantity -= quantity

    db.session.add(order)
    db.session.commit()
    return jsonify(order.to_dict())


@product_routes.route('/all')
def all_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])