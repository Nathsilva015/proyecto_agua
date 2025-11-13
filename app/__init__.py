from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from app import models, routes
    with app.app_context():
        db.create_all()

    # ✅ Aquí dentro ya existe 'app', por eso no da error
    from app.routes import init_routes
    init_routes(app)

    return app
