from flask import Blueprint

user_routes = Blueprint('user_routes', __name__,url_prefix='/users')
@user_routes.route('/')
def test():
    return 'Hey from users route!'