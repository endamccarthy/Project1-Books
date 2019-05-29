from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


class SearchForm(FlaskForm):
    choices = [('', 'Select Category'),
               ('ISBN', 'ISBN'),
               ('title', 'Title'),
               ('author', 'Author')]
    select = SelectField('Enter Book Information:', choices=choices, default='')
    search = StringField('Enter search query', validators=[DataRequired()])
    submit = SubmitField('Search')


class ReviewForm(FlaskForm):
    choices = [('', 'Rate Book'),
               ('1', '1'),
               ('2', '2'),
               ('3', '3'),
               ('4', '4'),
               ('5', '5')]
    select = SelectField('Rating out of 5:', choices=choices, default='')
    review = StringField('Write a Review', validators=[Length(min=1, max=255, message='Too many characters! (max 255)')])
    submit = SubmitField('Submit Review')