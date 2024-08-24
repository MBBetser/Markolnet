from flask import Flask
import os
from . import db
from .routes import all_blueprints
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'handy.sqlite')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    for blueprint in all_blueprints:
        app.register_blueprint(blueprint)

    app.run(debug=True)   
    @app.route('/')
    def test():
        return 'Hey from main route!'
    return app

