import os
import requests

from flask import Flask, session, request, render_template, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
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
    # save the above valus in the database
    db.execute("INSERT INTO users (fname, lname, email, username, password) VALUES \
    (:fname, :lname, :email, :username, :password)",
    {"fname": first_name, "lname" : last_name, "email": email, "username" :username, "password" :password})
    # db.execute("INSERT INTO mapping (user_id) VALUES (:user_id)", {"user_id": })
    db.commit()
    return render_template("login.html")

@app.route("/login" , methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    email = request.form.get("email")
    password = request.form.get("password")
    result = db.execute("SELECT password FROM users WHERE email = :email", {"email": email}).fetchall()
    print(result)
    # [('password',)]

    if password == result[0][0]:
        return redirect(url_for('search'))
    else:
        message = "You entered wrong credentials"
        return render_template("login.html", message=message)

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")

    isbn = request.form.get("isbn")
    title = request.form.get("title")
    author = request.form.get("author")

    if isbn == '' and title == '':
        books = db.execute("SELECT * from books WHERE author LIKE :author", {"author": '%'+author+'%'}).fetchall()
    elif isbn == '' and author == '':
        books = db.execute("SELECT * from books WHERE title LIKE :title", {"title": '%'+title+'%'}).fetchall()
    elif title == '' and author == '':
        books = db.execute("SELECT * from books WHERE isbn LIKE :isbn", {"isbn": '%'+isbn+'%'}).fetchall()
    elif isbn == '':
        books = db.execute("SELECT * from books WHERE \
        title LIKE :title OR author LIKE :author", {"title": '%'+title+'%', "author": '%'+author+'%'}).fetchall()
    elif title == '':
        books = db.execute("SELECT * from books WHERE \
        isbn LIKE :isbn OR author LIKE :author", {"isbn": '%'+isbn+'%', "author": '%'+author+'%'}).fetchall()
    elif author == '':
        books = db.execute("SELECT * from books WHERE \
        isbn LIKE :isbn OR title LIKE :title", {"isbn": '%'+isbn+'%', "title": '%'+title+'%'}).fetchall()
    elif isbn != '' and title != '' and author != '':
        books = db.execute("SELECT * from books WHERE \
            isbn LIKE :isbn OR title LIKE :title OR author LIKE :author",
            {"isbn": '%'+isbn+'%', "title": '%'+title+'%', "author": '%'+author+'%'}).fetchall()
    else:
        books = list()

    if len(books) == 0:
        message = "No books found on your search criteria"
        return render_template("search.html", message=message)

    success = "Here are they:"
    return render_template("search.html", books=books, success=success, count=len(books))

@app.route("/book/<isbn>")
def get_book(isbn):
    # isbn = "000100039X"
    books = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "JbJvaGJSOPbkd6SGvajpw", "isbns": isbn })
    books = books.json()

    book = db.execute("SELECT * from books WHERE isbn = :isbn", {"isbn": isbn}).fetchall()
    average_rating = books['books'][0]['average_rating']
    ratings_count = books['books'][0]['work_ratings_count']

    return render_template("book.html", average_rating=average_rating, ratings_count=ratings_count, book=book)

@app.route("/review")
def review():
    pass

@app.route("/logout")
def logout():
    # alert that you have been successfully logged out
    return render_template("index.html")
