from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_user
from core import db, bcrypt
from core.users.forms import (RegistrationForm, LoginForm)


# 'users' will be the name of the blueprint
users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
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


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.execute("SELECT * FROM users WHERE email=(:email) FETCH FIRST ROW ONLY", {"email": form.email.data})
        for row in user:
            user_password = row["password"]
        if user and bcrypt.check_password_hash(user_password, form.password.data):
            login_user(user, remember=form.remember.data)
            # if a link is clicked that requires a user to be logged in, this will redirect to that link after login otherwise 'main.home'
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


