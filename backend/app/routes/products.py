from flask import Blueprint

product_routes = Blueprint('product_routes', __name__,url_prefix='/products')
@product_routes.route('/')
def test():
    return 'Hey from products route!'