import os

from flask import Flask

from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def main():
    try:
        db.create_all()
        print("Successfully created tables")
    except:
        print("An error occurred")


if __name__ == "__main__":
    with app.app_context():
        main()
