from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    """
    Represents an author in the library database.

    Attributes:
        id (int): The unique identifier of the author (primary key, auto-incrementing).
        name (str): The author's name (not nullable, maximum length 100 characters).
        birth_date (date): The author's date of birth (nullable).
        date_of_death (date, optional): The author's date of death (nullable).

    Relationships:
        books (list of Book): A list of books written by this author (backref).

    Methods:
        __repr__() (str): Returns a string representation of the Author object
            for debugging and logging purposes.
    """
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date)
    date_of_death = db.Column(db.Date, nullable=True)

def __repr__(self):
        return f"Author(id={self.id}, name={self.name}, \
                birth_date={self.birth_date}, date_of_death={self.date_of_death})"


class Book(db.Model):
    """
    Represents a book in the library database.

    Attributes:
        id (int): The unique identifier of the book (primary key, auto-incrementing).
        isbn (str): The ISBN code of the book (not nullable, maximum length 100 characters).
        title (str): The title of the book (not nullable, maximum length 100 characters).
        publication_year (date): The year of publication of the book.
        author_id (int): The foreign key referencing the author of the book.

    Relationships:
        author (Author): The Author object associated with this book (relationship).

    Methods:
        __repr__() (str): Returns a string representation of the Book object
            for debugging and logging purposes.
    """
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Date)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    author = db.relationship("Author", backref="books")
    
    def __repr__(self):
        return f"Book(id={self.id}, isbn='{self.isbn}', title='{self.title}', \
                publication_year={self.publication_year}, author_id={self.author_id})"
