from flask import Blueprint, render_template, session, g
from core.main.forms import SearchForm
from core import db
from wtforms.validators import ValidationError
import requests
import urllib.parse


# 'main' will be the name of the blueprint
main = Blueprint('main', __name__)


@main.before_request
def before_request():
    g.user_id = None
    if "user_id" in session:
        g.user_id = session["user_id"]


@main.route("/", methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        books = db.execute("SELECT * FROM books WHERE isbn=(:isbn) FETCH FIRST ROW ONLY", {"isbn": form.number.data})
        """
        for book in books:
            book_title = book["title"]
            book_author = book["author"]
            book_year = book["year"]
            book_isbn = book["isbn"]
        """
        book = lookup(form.number.data)
        book_id = book["id"]
        book_average_rating = book["average_rating"]
        return render_template("home.html", title="Search Results", legend="Search Results", book_id=book_id, 
                                book_average_rating=book_average_rating, books=books, form=form)
    return render_template('home.html', title="Home", legend="Search Books", form=form)


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
            "average_rating": bookInfo["average_rating"],
            "work_ratings_count": bookInfo["work_ratings_count"]
        }
    except (KeyError, TypeError, ValueError):
        return None