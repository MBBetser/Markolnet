from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from ..models import Store, StoreProduct, Product
from ..db import db
from flask_login import current_user
store_routes = Blueprint('stores_route', __name__, url_prefix='/stores')
@store_routes.route('/')
def stores():
    stores = Store.query.all()
    return render_template('all_stores.html', stores=stores)

# CREATE STORE MODIFY
@store_routes.route('/create', methods=['POST'])
def create_store():
    print('create store')
    data = request.get_json()
    owner_id = data.get('owner_id')
    name = data.get('name')
    if not owner_id or not name:
        return jsonify({"message": "Missing owner_id or name"}), 400
    
    if Store.query.filter_by(name=name).first():
        return jsonify({"message": "Store already exists"}), 400
    else:
        store = Store(owner_id=owner_id, name=name)
        db.session.add(store)
        db.session.commit()
        return jsonify(store.to_dict()), 200


@store_routes.route('/<int:store_id>')
def store(store_id, methods=['GET']):
    store = Store.query.get(store_id)
    if not store:
        return jsonify({"message": "Store not found"}), 404
    available_products = Product.query.all()
    return render_template('store.html', store=store, current_user=current_user, available_products=available_products)


# ADD PRODUCTS--------------------
@store_routes.route('/<int:store_id>/product/add-<int:product_id>', methods=['POST'])
def add_product(store_id, product_id):
    print('add product')
    data = request.get_json()
    print('error here')
    quantity = data.get('quantity')
    price = data.get('price')
    store = Store.query.get(store_id)

    if not store:
        print('store not found')
        return jsonify({"message": "Store not found"}), 404
    
    if not product_id:
        print('product not found')
        return jsonify({"message": "Product not found"}), 404
    
    if not quantity:
        print('quantity not found')
        return jsonify({"message": "Quantity not found"}), 404
    
    if StoreProduct.query.filter_by(store_id=store_id, product_id=product_id).first():
        store_product = StoreProduct.query.filter_by(store_id=store_id, product_id=product_id).first()
        store_product.quantity += quantity
        if price != store_product.price:
            store_product.price = price
        db.session.commit()
        return jsonify({"redirect_url":url_for('stores_route.store', store_id=store_id)})
    
    store_product = StoreProduct(
        store_id=store_id,
        product_id=product_id,
        quantity=quantity,
        price=price
    )
    store.products.append(store_product)
    db.session.add(store_product)
    db.session.commit()
    return jsonify({"redirect_url":url_for('stores_route.store', store_id=store_id)})

@store_routes.route('/<int:store_id>/product/add-products', methods=['POST'])
def add_product_from_web(store_id):
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    price = 10
    store = Store.query.get(store_id)
    store_product = StoreProduct(
        store_id=store_id,
        product_id=product_id,
        quantity=quantity,
        price=price
    )
    store.products.append(store_product)
    db.session.add(store_product)
    db.session.commit()
    return jsonify(store.to_dict())
