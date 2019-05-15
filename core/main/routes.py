from flask import Blueprint, render_template
from core.main.forms import BookForm
from wtforms.validators import ValidationError
import requests
import urllib.parse


# 'main' will be the name of the blueprint
main = Blueprint('main', __name__)


@main.route("/", methods=['GET', 'POST'])
def index():
    form = BookForm()
    if not form.validate_on_submit():
        book = lookup(form.symbol.data)
        book_id = book["id"]
        book_isbn = book["isbn"]
        book_average_rating = book["average_rating"]
        return render_template("home.html", title="Quoted", book_id=book_id, book_isbn=book_isbn, book_average_rating=book_average_rating, form=form)
    return render_template('home.html', title="Quote", form=form)


def lookup(isbn):
    # Contact API
    try:
        response = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "wIAPr4dgJufQmdB00Uww", "isbns": f"{urllib.parse.quote_plus(isbn)}"})
        response.raise_for_status()
    except requests.RequestException:
        return None
    # Parse response
    try:
        book = response.json()
        bookInfo = book["books"][0]
        return {
            "id": bookInfo["id"],
            "isbn": bookInfo["isbn"],
            "average_rating": bookInfo["average_rating"]
        }
    except (KeyError, TypeError, ValueError):
        return None