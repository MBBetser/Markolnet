from flask import Blueprint

store_routes = Blueprint('stores_route', __name__, url_prefix='/stores')
@store_routes.route('/')
def test():
    return 'Hey from stores route!'