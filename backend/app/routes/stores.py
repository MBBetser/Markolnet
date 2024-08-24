from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from ..models import Store, StoreProduct
from ..db import db
store_routes = Blueprint('stores_route', __name__, url_prefix='/stores')
@store_routes.route('/')
def test():
    return 'Hey from stores route!'

# CREATE STORE MODIFY
@store_routes.route('/create', methods=['POST'])
def create_store():
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
        return jsonify(store.to_dict())


# UPDATE STORE MODIFY
@store_routes.route('/delete/<int:store_id>', methods=['DELETE'])
def delete_store(store_id):
    store = Store.query.get(store_id)
    db.session.delete(store)
    db.session.commit()
    return jsonify({"message": "Store deleted"})


@store_routes.route('/<int:store_id>')
def store(store_id, methods=['GET']):
    data = request.get_json()
    store = Store.query.get(store_id)
    return jsonify(store.to_dict())

# ADD PRODUCTS--------------------

@store_routes.route('/<int:store_id>/product/add-<int:product_id>', methods=['POST'])
def add_product(store_id, product_id):
    data = request.get_json()
    quantity = data.get('quantity')
    store = Store.query.get(store_id)
    store.products.append(StoreProduct(product_id=product_id, quantity=quantity))
    db.session.commit()
    return jsonify(store.to_dict())


@store_routes.route('/all')
def all_stores():
    stores = Store.query.all()
    return jsonify([store.to_dict() for store in stores])