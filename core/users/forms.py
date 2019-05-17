import re
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from core.models import User
from core import bcrypt
from core import db


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        
        user = db.execute("SELECT * FROM books ")

"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
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
"""