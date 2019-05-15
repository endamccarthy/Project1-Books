import requests
import urllib.parse
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


def validateBook(form, field):
    # Contact API
    try:
        response = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "wIAPr4dgJufQmdB00Uww", "isbns": f"{urllib.parse.quote_plus(field.data)}"})
        response.raise_for_status()
    except requests.RequestException:
        raise ValidationError('Invalid! Please choose a valid isbn.')


class BookForm(FlaskForm):
    symbol = StringField('Enter book ISBN:', validators=[DataRequired(), validateBook])
    submit = SubmitField('Enter')