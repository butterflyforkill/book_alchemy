from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from data_models import db, Author, Book



app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_unique_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.sqlite'
db.init_app(app)


@app.route('/')
def home():
    books = Book.query.join(Author).all()  # Join Book and Author tables
    return render_template('home.html', books=books)


@app.route('/add_author', methods = ['GET', 'POST'])
def add_author():
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
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()

    flash(f"Book '{book.title}' successfully deleted.", 'success')
    return redirect(url_for('home'))


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
