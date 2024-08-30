from flask import Blueprint

order_routes = Blueprint('order_routes', __name__,url_prefix='/orders')

@order_routes.route('/')
def test():
    return 'Hey from orders route!'