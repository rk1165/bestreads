## Book Search and Review Website

- Project developed when learning about flask, SQLAlchemy
- Users can register to search and review books.
- It stores the books listed in `books.csv` file in the database.
- The app searches for a book based on ISBN, Title or Author from the books stored in the database
- The book's review can be fetched from Goodreads and the user can add review comment.

### How to run the app locally?
- run `pip install -r requirements.txt` to install the required libraries.
- Then run `bash load_data.sh` to load the data in the database.
- Finally, run the app locally by executing `bash run.sh` script
