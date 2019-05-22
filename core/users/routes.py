from flask import render_template, url_for, flash, redirect, request, Blueprint, session, g
from core import db, bcrypt
from core.users.forms import RegistrationForm, LoginForm


# 'users' will be the name of the blueprint
users = Blueprint('users', __name__)


@users.before_request
def before_request():
    g.user_id = None
    if "user_id" in session:
        g.user_id = session["user_id"]


@users.route("/register", methods=['GET', 'POST'])
def register():
    if "user_id" in session:
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
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if "user_id" in session:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        session.pop("user_id", None)
        user = db.execute("SELECT * FROM users WHERE email=(:email) FETCH FIRST ROW ONLY", {"email": form.email.data})
        for row in user:
            user_password = row["password"]
            user_id = row["id"]
        if user and bcrypt.check_password_hash(user_password, form.password.data):
            session["user_id"] = user_id
            # if a link is clicked that requires a user to be logged in, this will redirect to that link after login otherwise 'main.home'
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for('main.index'))


@users.route("/test")
def test():
    if g.user_id:
        return render_template('test.html')
    return redirect(url_for('users.login'))
