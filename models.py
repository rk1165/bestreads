from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Book(db.Model):
    __tablename__ = "books"
    isbn = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    year = db.Column(db.Integer, nullable=False)


# class Mapping(db.Model):
#     __tablename__ = "mapping"
#     id = db.Column(db.Integer, primary_key = True)
#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
#     book_id = db.Column(db.String(15), db.ForeignKey("books.isbn"), nullable = False)

class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    # rating = db.Column(db.Float, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.String(15), db.ForeignKey("books.isbn"), nullable=False)
    review = db.Column(db.String(500), nullable=False)
