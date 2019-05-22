import requests
import urllib.parse
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
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
    number = StringField('Search ISBN:', validators=[Optional()])
    title = StringField('Search titles:', validators=[Optional()])
    author = StringField('Search authors:', validators=[Optional()])
    submit = SubmitField('Enter')

    def validate(self):
        if not super(SearchForm, self).validate():
            return False
        if not self.number.data and not self.title.data and not self.author.data:
            msg = 'At least one field needs to be filled out!'
            self.number.errors.append(msg)
            self.title.errors.append(msg)
            self.author.errors.append(msg)
            self.submit.errors.append(msg)
            return False
        return True