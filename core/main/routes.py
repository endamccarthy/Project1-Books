from flask import Blueprint, render_template, session, g, flash, redirect, request
from core.main.forms import SearchForm, ReviewForm
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
        search_string = form.search.data
        field = form.select.data
        """
        In order to use the LIKE operator (to search for part of a query) together with the bind variable we need to
        add a % before and after the query. The % need to be included in the quotes like this: '%query%'.
        """
        if field == 'ISBN':
            qry = db.execute("SELECT * FROM books WHERE isbn LIKE (:isbn)", {"isbn": ("%" + search_string + "%")})
        elif field == 'title':
            qry = db.execute("SELECT * FROM books WHERE LOWER(title) LIKE LOWER(:title)", {"title": ("%" + search_string + "%")})
        else:
            qry = db.execute("SELECT * FROM books WHERE LOWER(author) LIKE LOWER(:author)", {"author": ("%" + search_string + "%")})

        if qry.rowcount == 0:
            flash('No results found!', 'danger')
            return redirect('/')
        elif qry.rowcount > 100:
            flash('Too many results! Please be more specific', 'danger')
            return redirect('/')
        else:
            return render_template("home.html", title="Search Results", legend="Search Results", qry=qry, form=form)
    return render_template('home.html', title="Home", legend="Search Books", form=form)


@main.route("/book/<string:isbn>", methods=['GET', 'POST'])
def book(isbn):
    books = db.execute("SELECT * FROM books WHERE isbn=(:isbn) FETCH FIRST ROW ONLY", {"isbn": isbn})
    for book in books:
        book_title = book["title"]
        author = book["author"]
        year = book["year"]
    book = lookup(isbn)
    average_rating = book["average_rating"]
    ratings_count = book["work_ratings_count"]
    form = ReviewForm()
    username = db.execute("SELECT username FROM users WHERE id=(:id) FETCH FIRST ROW ONLY", {"id": g.user_id})
    for row in username:
        username = row[0]
    
    test = db.execute("SELECT * FROM reviews WHERE username=(:username) FETCH FIRST ROW ONLY", {"username": username})
    if test.rowcount > 0:
        print('test1')

    existing_reviews = db.execute("SELECT * FROM reviews WHERE book_isbn=(:isbn)", {"isbn": isbn})
    if existing_reviews.rowcount == 0:
        existing_reviews = None
    # add review to database if form is submitted
    if form.validate_on_submit():
        rating = form.select.data
        review = form.review.data
        db.execute("INSERT INTO reviews (book_isbn,username,rating,review) VALUES (:book_isbn,:username,:rating,:review)",
                    {"book_isbn":isbn, 
                     "username":username, 
                     "rating":rating,
                     "review":review})
        db.commit()
        existing_reviews = db.execute("SELECT * FROM reviews WHERE book_isbn=(:isbn)", {"isbn": isbn})
        return render_template('book.html', title="Book Info", legend="Book Info", isbn=isbn, book_title=book_title, existing_reviews=existing_reviews,
                                author=author, year=year, average_rating=average_rating, ratings_count=ratings_count, username=username, form=form)

    return render_template('book.html', title="Book Info", legend="Book Info", isbn=isbn, book_title=book_title, existing_reviews=existing_reviews,
                            author=author, year=year, average_rating=average_rating, ratings_count=ratings_count, username=username, form=form)


def lookup(isbn):
    # contact API
    try:
        response = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "wIAPr4dgJufQmdB00Uww", "isbns": f"{urllib.parse.quote_plus(isbn)}"})
        response.raise_for_status()
    except requests.RequestException:
        return None
    # parse response
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



"""
@main.route("/", methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        books = db.execute("SELECT * FROM books WHERE isbn=(:isbn) FETCH FIRST ROW ONLY", {"isbn": form.number.data})
        book = lookup(form.number.data)
        book_id = book["id"]
        book_average_rating = book["average_rating"]
        return render_template("home.html", title="Search Results", legend="Search Results", book_id=book_id, 
                                book_average_rating=book_average_rating, books=books, form=form)
    return render_template('home.html', title="Home", legend="Search Books", form=form)
"""