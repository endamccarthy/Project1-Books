import os
from flask import Flask, session
from flask_session import Session
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from core.config import Config


# Database setup
if not os.getenv("HEROKU_DATABASE_URL"):
    raise RuntimeError("HEROKU_DATABASE_URL is not set")
engine = create_engine(os.getenv("HEROKU_DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    Session(app)

    bcrypt.init_app(app)

    date = '2019-06-24'

    # create users table
    db.execute("CREATE TABLE IF NOT EXISTS users (\
                id SERIAL PRIMARY KEY, \
                username VARCHAR(20) NOT NULL UNIQUE, \
                email VARCHAR(120) NOT NULL UNIQUE, \
                password VARCHAR(255))")
    db.execute("CREATE TABLE IF NOT EXISTS reviews (\
                id SERIAL PRIMARY KEY, \
                book_isbn VARCHAR(13) NOT NULL REFERENCES books (isbn), \
                user_id VARCHAR(20) NOT NULL REFERENCES users (id), \
                rating INT NOT NULL, \
                review VARCHAR(255), \
                date_posted DATE NOT NULL DEFAULT :date", {"date":date})
    db.commit()

    # Blueprints setup
    from core.main.routes import main
    from core.users.routes import users
    app.register_blueprint(main)
    app.register_blueprint(users)

    return app