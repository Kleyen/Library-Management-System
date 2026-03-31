from app.extensions import db
from datetime import datetime


class Book(db.Model):
    __tablename__ = 'books'

    # Primary Key
    id             = db.Column(db.Integer, primary_key=True)

    # Fields - edit values as needed
    title          = db.Column(db.String(200), nullable=False)
    author         = db.Column(db.String(200), nullable=False)
    isbn           = db.Column(db.String(20), unique=True, nullable=False)
    genre          = db.Column(db.String(100), nullable=True)
    published_year = db.Column(db.Integer, nullable=True)
    quantity       = db.Column(db.Integer, nullable=False, default=1)
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to loans table
    loans = db.relationship('Loan', backref='book', lazy=True)

    def __repr__(self):
        return f'<Book {self.title}>'

    # ------------------------------------------------------- #
    # ------------------------------------------------------- #

    @property
    def available_copies(self):
        active_loans = sum(1 for loan in self.loans if loan.status == 'active')
        return self.quantity - active_loans

    @property
    def is_available(self):
        return self.available_copies > 0