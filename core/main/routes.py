from flask import Blueprint, render_template, session, g, flash, redirect, request, url_for, jsonify, abort
from core.main.forms import SearchForm, ReviewForm
from core import db
from wtforms.validators import ValidationError
import requests
import urllib.parse


# 'main' will be the name of the blueprint
main = Blueprint('main', __name__)


# this is carried out once a request is made, it checks if the user is logged in
@main.before_request
def before_request():
    g.user_id = None
    if "user_id" in session:
        g.user_id = session["user_id"]


@main.route("/", methods=['GET', 'POST'])
def index():
    if g.user_id == None:
        return redirect(url_for('users.login'))
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
    if g.user_id == None:
        return redirect(url_for('users.login'))

    # get book information from database using isbn number 
    books = db.execute("SELECT * FROM books WHERE isbn=(:isbn) FETCH FIRST ROW ONLY", {"isbn": isbn})
    for book in books:
        book_title = book["title"]
        author = book["author"]
        year = book["year"]
    
    # get book information from Goodreads API using lookup function
    book = lookup(isbn)
    average_rating = book["average_rating"]
    ratings_count = book["work_ratings_count"]

    form = ReviewForm()

    # get username of user
    username = db.execute("SELECT username FROM users WHERE id=(:id) FETCH FIRST ROW ONLY", {"id": g.user_id})
    for row in username:
        username = row[0]
    
    # check if the user has already left a review for this book
    already_reviewed = False
    rows = db.execute("SELECT * FROM reviews WHERE username=(:username) and book_isbn=(:isbn) FETCH FIRST ROW ONLY", {"username": username, "isbn": isbn})
    if rows.rowcount > 0:
        already_reviewed = True

    # get all reviews for this book from all users
    existing_reviews = db.execute("SELECT * FROM reviews WHERE book_isbn=(:isbn)", {"isbn": isbn})
    if existing_reviews.rowcount == 0:
        existing_reviews = None

    # add review to database if form is submitted
    if form.validate_on_submit():
        rating = form.select.data
        review = form.review.data
        if already_reviewed == False:
            db.execute("INSERT INTO reviews (book_isbn,username,rating,review) VALUES (:book_isbn,:username,:rating,:review)",
                        {"book_isbn":isbn, 
                        "username":username, 
                        "rating":rating,
                        "review":review})
            db.commit()
        existing_reviews = db.execute("SELECT * FROM reviews WHERE book_isbn=(:isbn)", {"isbn": isbn})
        already_reviewed = True
        return render_template('book.html', title="Book Info", legend="Book Info", isbn=isbn, book_title=book_title, author=author, 
                                year=year, average_rating=average_rating, ratings_count=ratings_count, username=username, 
                                existing_reviews=existing_reviews, already_reviewed=already_reviewed)

    return render_template('book.html', title="Book Info", legend="Book Info", isbn=isbn, book_title=book_title, author=author, 
                            year=year, average_rating=average_rating, ratings_count=ratings_count, username=username, 
                            existing_reviews=existing_reviews, already_reviewed=already_reviewed, form=form)


@main.route("/api/<string:isbn>")
def api_request(isbn):
    books = db.execute("SELECT * FROM books WHERE isbn=(:isbn) FETCH FIRST ROW ONLY", {"isbn": isbn})
    if books.rowcount == 0:
        abort(404)
    for book in books:
        title = book["title"]
        author = book["author"]
        year = book["year"]
    reviews = db.execute("SELECT * FROM reviews WHERE book_isbn=(:isbn)", {"isbn": isbn})
    review_count = float(reviews.rowcount)
    total = 0.0
    if review_count == 0:
        average_score = 0.0
    else:
        for review in reviews:
            total = total + float(review["rating"])
        average_score = total/review_count
    return jsonify(title=title,
                   author=author,
                   year=year,
                   isbn=isbn,
                   review_count=review_count,
                   average_score=average_score)


@main.route("/contact")
def contact():
    return render_template("contact.html")


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