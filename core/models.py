from core import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    user = db.execute("SELECT * FROM users WHERE id=(:id) FETCH FIRST ROW ONLY", {"id": int(user_id)})
    return user
    

class User(db.Model, UserMixin):

    # create users table
    db.execute("CREATE TABLE IF NOT EXISTS users (\
                id SERIAL PRIMARY KEY, \
                username VARCHAR(20) NOT NULL UNIQUE, \
                email VARCHAR(120) NOT NULL UNIQUE, \
                password VARCHAR(255))")
    db.commit()
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
