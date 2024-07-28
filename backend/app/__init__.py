from flask import Flask
import os
from . import db
from .routes import all_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'handy.sqlite'),
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    db.init_app(app)
    for blueprint in all_blueprints:
        app.register_blueprint(blueprint)
    @app.route('/')
    def test():
        return 'Hey from main route!'
    return app

