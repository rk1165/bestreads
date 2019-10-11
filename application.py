import os

import requests
from flask import Flask, session, request, render_template, redirect, url_for, jsonify
from sqlalchemy import and_, or_

from flask_session import Session
from models import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    session['logged_in'] = False
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("registration.html")

    first_name = request.form.get("firstName")
    last_name = request.form.get("lastName")
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")

    # Saving the above values into the database
    user = User(fname=first_name, lname=last_name, email=email, username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    password = request.form.get("password")
    user = User.query.filter(and_(User.email == email, User.password == password)).all()

    if len(user) > 0 and password == user[0].password:
        session['logged_in'] = True
        session['user'] = email
        session['password'] = password
        return redirect(url_for('search'))
    else:
        message = "Invalid credentials"
        return render_template("login.html", message=message)


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")

    isbn = request.form.get("isbn")
    title = request.form.get("title")
    author = request.form.get("author")

    books = list()
    # Can this be somehow made less verbose
    if isbn == '' and title == '':
        books = Book.query.filter(Book.author.like("%" + author + "%")).all()
    elif isbn == '' and author == '':
        books = Book.query.filter(Book.title.like("%" + title + "%")).all()
    elif title == '' and author == '':
        books = Book.query.filter(Book.isbn.like("%" + isbn + "%")).all()
    elif isbn == '':
        books = Book.query.filter(or_(Book.title.like("%" + title + "%"), Book.author.like("%" + author + "%"))).all()
    elif title == '':
        books = Book.query.filter(or_(Book.isbn.like("%" + isbn + "%"), Book.author.like("%" + author + "%"))).all()
    elif author == '':
        books = Book.query.filter(or_(Book.title.like("%" + title + "%"), Book.isbn.like("%" + isbn + "%"))).all()
    elif isbn != '' and title != '' and author != '':
        books = Book.query.filter(or_(Book.title.like("%" + title + "%"), Book.title.like("%" + author + "%"),
                                      Book.isbn.like("%" + isbn + "%"))).all()

    if len(books) == 0:
        message = "No books found on your search criteria"
        return render_template("search.html", message=message)

    success = "Here are they:"
    return render_template("search.html", books=books, success=success, count=len(books))


@app.route("/book/<isbn>")
def get_book(isbn):
    books = requests.get("https://www.goodreads.com/book/review_counts.json", params={"isbns": isbn})
    books = books.json()

    book = Book.query.get(isbn)
    reviews = Review.query.filter(Review.book_id == isbn).all()

    average_rating = books['books'][0]['average_rating']
    ratings_count = books['books'][0]['work_ratings_count']

    return render_template("book.html", average_rating=average_rating,
                           ratings_count=ratings_count, book=book, reviews=reviews)


# This returns a backend response to anyone consuming our API
@app.route("/api/book/<isbn>")
def book_api(isbn):
    books = requests.get("https://www.goodreads.com/book/review_counts.json", params={"isbns": isbn})
    books = books.json()
    average_rating = books['books'][0]['average_rating']
    ratings_count = books['books'][0]['work_ratings_count']

    book = Book.query.get(isbn)
    if book is None:
        return jsonify({"error": "Invalid ISBN"}), 422
    return jsonify({
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": isbn,
        "review_count": ratings_count,
        "average_score": average_rating
    })


@app.route("/review/<isbn>", methods=["GET", "POST"])
def review(isbn):
    user = User.query.filter(User.email == session['user']).all()
    user_id = user[0].id
    review_form = request.form.get('review')
    r = Review.query.filter(Review.user_id == user_id).all()

    user_review = Review(user_id=user_id, book_id=isbn, review=review_form)
    if len(r) > 0:
        message = "You have already reviewed the book"
        session['messages'] = message
        return redirect(url_for('get_book', isbn=isbn))

    db.session.add(user_review)
    db.session.commit()
    return redirect(url_for('get_book', isbn=isbn))


@app.route("/logout")
def logout():
    # alert that you have been successfully logged out
    session['logged_in'] = False

    return render_template("index.html")
