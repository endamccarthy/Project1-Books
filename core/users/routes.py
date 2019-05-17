from flask import render_template, url_for, flash, redirect, request, Blueprint
#from flask_login import current_user
from core import db, bcrypt
from core.users.forms import (RegistrationForm)


# 'users' will be the name of the blueprint
users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.execute("INSERT INTO users (username,email,password) VALUES (:username,:email,:password)",
                    {"username":form.username.data, 
                     "email":form.email.data, 
                     "password":hashed_password})
        db.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        #flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('main.index'))
    return render_template('register.html', title='Register', form=form)