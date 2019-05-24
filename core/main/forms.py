from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


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