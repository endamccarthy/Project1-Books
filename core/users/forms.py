import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from core import db


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        users = db.execute("SELECT * FROM users WHERE username=(:username) FETCH FIRST ROW ONLY", {"username": username.data})
        for user in users:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        users = db.execute("SELECT * FROM users WHERE email=(:email) FETCH FIRST ROW ONLY", {"email": email.data})
        for user in users:
            raise ValidationError('That email is taken. Please choose a different one.')

    def validate_password(self, password):
        while True:
            if len(password.data) < 8:
                raise ValidationError("Make sure your password is at least 8 letters.")
            elif re.search('[0-9]',password.data) is None:
                raise ValidationError("Make sure your password has a number in it.")
            elif re.search('[A-Z]',password.data) is None: 
                raise ValidationError("Make sure your password has a capital letter in it.")
            else:
                break