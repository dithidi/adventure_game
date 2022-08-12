from application import db
from sqlalchemy import func

categories = db.Table('book_genre',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)
    title = db.Column(db.String(256))
    email = db.Column(db.String(128))
    password = db.Column(db.String(128))
    date_published = db.Column(db.DateTime)
    date_added = db.Column(db.DateTime, default=func.now())

    user = db.relationship('User', backref='books', lazy=True)
    author = db.relationship('Author', backref='books', lazy=True)
    genre = db.relationship('Genre', backref='books', lazy=True)
    categories = db.relationship('Category', secondary=categories, lazy='subquery',
        backref=db.backref('books', lazy=True))

    def __init__(self, author_id, title, date_published):
        self.author_id = author_id
        self.title = title
        self.date_published = date_published

    def __repr__(self):
        return '<id {}>'.format(self.id)
