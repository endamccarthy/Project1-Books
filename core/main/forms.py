import requests
import urllib.parse
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Optional


"""
def validateBook(form, field):
    # Contact API
    try:
        response = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "wIAPr4dgJufQmdB00Uww", "isbns": f"{urllib.parse.quote_plus(field.data)}"})
        response.raise_for_status()
    except requests.RequestException:
        raise ValidationError('Invalid! Please choose a valid isbn.')
"""


class SearchForm(FlaskForm):
    choices = [('', 'Select Category'),
               ('ISBN', 'ISBN'),
               ('title', 'Title'),
               ('author', 'Author')]
    select = SelectField('Enter Book Information:', choices=choices, default='')
    search = StringField('Enter search query', validators=[DataRequired()])
    submit = SubmitField('Search')