import os
from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from core.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    if not os.getenv("HEROKU_DATABASE_URL"):
        raise RuntimeError("HEROKU_DATABASE_URL is not set")

    Session(app)

    # Database setup
    engine = create_engine(os.getenv("HEROKU_DATABASE_URL"))
    db = scoped_session(sessionmaker(bind=engine))

    # Blueprints setup
    from core.main.routes import main
    app.register_blueprint(main)

    return app