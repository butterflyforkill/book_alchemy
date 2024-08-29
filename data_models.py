from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date)
    date_of_death = db.Column(db.Date, nullable=True)

def __str__(self):
        return f"Author(id={self.id}, name={self.name},birth_date={self.birth_date}, date_of_death={self.date_of_death})"


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Date)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    author = db.relationship("Author", backref="books")
    
    def __repr__(self):
        return f"Book(id={self.id}, isbn='{self.isbn}', title='{self.title}', publication_year={self.publication_year}, author_id={self.author_id})"
