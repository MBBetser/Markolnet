from flask import Flask, render_template, session
import os
from . import db
from .models import User
from .routes import all_blueprints
from flask_login import LoginManager, logout_user


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'handy.sqlite')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    login_manager = LoginManager(app)
    login_manager.login_view = 'user_routes.login'
    login_manager.init_app(app)
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


    if __name__ == '__main__':
        app.run()

    @app.route('/')
    def index():
        return render_template('index.html')
    
    
    return app

