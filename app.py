import os
from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import datetime
from data_models import db, Author, Book

# Inisialization of the app and config of the DB
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_unique_secret_key'
db_path = os.path.join(os.getcwd(), 'data', 'library.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db.init_app(app)


# Backend API endpoints 
@app.route('/')
def home():
    """
    Renders the home page with a list of all books in the library,
    fetched through a join query between Book and Author tables.

    Returns:
        Template: 'home.html' with books data
    """
    books = Book.query.join(Author).all()  # Join Book and Author tables
    return render_template('home.html', books=books)


@app.route('/add_author', methods = ['GET', 'POST'])
def add_author():
    """
    Handles requests for adding a new author to the library.

    - On GET requests, renders the 'add_author.html' template.
    - On POST requests, retrieves author data from the form,
      creates a new Author object, adds it to the database session,
      commits the session, and displays a success message.
    - Handles invalid request methods with a 405 error.

    Returns:
        Template: 'add_author.html' (GET or with success message on POST)
        405: Invalid request method
    """
    if request.method == 'GET':
        return render_template('add_author.html')  # Render form on GET request
    elif request.method == 'POST':
        name = request.form['name']  # Get author name from form
        birth_date = datetime.strptime(request.form['birthdate'], '%Y-%m-%d')
        if request.form['date_of_death'] == '':
            date_of_death = None
        else:
            date_of_death = datetime.strptime(request.form['date_of_death'], '%Y-%m-%d')
        new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
        db.session.add(new_author)
        db.session.commit()

        # Display success message
        message = f"Author '{name}' successfully added!"
        return render_template('add_author.html', message=message)  # Render form with success message
    else:
        return "Invalid request method", 405  # Handle invalid methods


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Handles requests for adding a new book to the library.

    - On GET requests, fetches all authors from the database
      and renders the 'add_book.html' template with the author list.
    - On POST requests, retrieves book data from the form,
      creates a new Book object, adds it to the database session,
      commits the session, and displays a success message.
    - Handles invalid request methods with a 405 error.

    Returns:
        Template: 'add_book.html' with authors data (GET) or success message (POST)
        405: Invalid request method
    """
    authors = Author.query.all()  # Fetch all authors from the database

    if request.method == 'GET':
        return render_template('add_book.html', authors=authors)  # Render form with authors
    elif request.method == 'POST':
        title = request.form['book_title']
        isbn_code = request.form['isbn']
        publication_year_str = request.form.get('publication_year')
        publication_year = datetime.strptime(publication_year_str, '%Y')
        print(publication_year)
        author_id = request.form['author']

        new_book = Book(title=title, isbn=isbn_code, publication_year=publication_year, author_id=author_id)
        db.session.add(new_book)
        db.session.commit()

        message = f"Book '{title}' successfully added!"
        return render_template('add_book.html', message=message, authors=authors)
    else:
        return "Invalid request method", 405


@app.route('/sort', methods=['POST'])
def sort_books():
    """
    Sorts the list of books based on the selected criteria (title or author)
    submitted through the POST request from the sort form.

    - Retrieves the sort criteria ('title' or 'author') from the form data.
    - Uses SQLAlchemy's `join` and `order_by` methods to sort books
      based on the selected criteria:
        - 'title': Sorts by book title (ascending order).
        - 'author': Sorts by author name (ascending order).
        - Default (no selection): Returns all books.
    - Renders the 'home.html' template with the sorted list of books.

    Returns:
        Template: 'home.html' with sorted books data
    """
    sort_by = request.form.get('sort-by')
    if sort_by == 'title':
        books = Book.query.join(Author).order_by(Book.title).all()
    elif sort_by == 'author':
        books = Book.query.join(Author).order_by(Author.name).all()
    else:
        books = Book.query.join(Author).all()

    return render_template('home.html', books=books)


@app.route('/search', methods=['POST'])
def search_books():
    """
    Searches the library for books based on the user's search query
    submitted through the POST request from the search form.

    - Retrieves the search query from the form data.
    - Uses SQLAlchemy's `filter` and `ilike` (case-insensitive like)
      to search for books whose title contains the search query (as a substring).
    - Joins the Book and Author tables to fetch complete book information.
    - If books are found matching the search query:
        - Renders the 'home.html' template with the search results.
    - If no books are found:
        - Flashes an informative message using Flask's `flash` function.
        - Renders the 'home.html' template without any search results.

    Returns:
        Template: 'home.html' with search results (if any) or a message
    """
    search_query = request.form.get('search_query')

    # Use SQLAlchemy's `filter` and `ilike` to perform case-insensitive search
    books = Book.query.filter(Book.title.ilike(f'%{search_query}%')).join(Author).all()

    if books:
        return render_template('home.html', books=books)
    else:
        flash('No books found matching the search query.', 'info')
        return render_template('home.html')


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """
    Deletes a book from the library based on the provided book ID.

    - Retrieves the book object with the specified ID using
      `Book.query.get_or_404(book_id)`. This raises a 404 error if the book is not found.
    - Deletes the book object from the database session using `db.session.delete(book)`.
    - Commits the changes to the database using `db.session.commit()`.
    - Flashes a success message with the deleted book's title using Flask's `flash` function.
    - Redirects the user to the homepage using `redirect(url_for('home'))`.

    Returns:
        Redirect: Redirects to the homepage after successful deletion.
    """
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()

    flash(f"Book '{book.title}' successfully deleted.", 'success')
    return redirect(url_for('home'))


if __name__ == "__main__":
    # creating the tables
    # with app.app_context():
    #     try:
    #         db.create_all()
    #         print("Tables created successfully.")
    #     except Exception as e:
    #         print(f"Error creating tables: {e}")
    app.run(debug=True)
