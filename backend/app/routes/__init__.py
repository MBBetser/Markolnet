from flask import Blueprint
from .users import user_routes
from .stores import store_routes
from .products import product_routes
from .orders import order_routes
from .cart import cart_routes
main_blueprint = Blueprint('main', __name__)

# Register individual route blueprints
main_blueprint.register_blueprint(user_routes)
main_blueprint.register_blueprint(store_routes)
main_blueprint.register_blueprint(product_routes)
main_blueprint.register_blueprint(order_routes)
main_blueprint.register_blueprint(cart_routes)

all_blueprints = [user_routes, store_routes, product_routes, order_routes, cart_routes]