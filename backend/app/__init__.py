from flask import Flask
import os
from . import db
import json

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
    
    @app.route('/')
    def test():
        return 'hey'

    db.init_app(app)

    return app

