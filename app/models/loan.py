from app.extensions import db
from datetime import datetime


class Loan(db.Model):
    __tablename__ = 'loans'

    # Primary Key
    id          = db.Column(db.Integer, primary_key=True)

    # Foreign Keys - links to books and members tables in library.db
    book_id     = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    member_id   = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)

    # Fields - edit values as needed
    borrow_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    due_date    = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)
    status      = db.Column(db.String(20), nullable=False, default='active')
    # status options: 'active', 'returned', 'overdue'

    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Loan book_id={self.book_id} member_id={self.member_id}>'

    # ------------------------------------------------------- #
    # ------------------------------------------------------- #

    @property
    def is_overdue(self):
        if self.status == 'returned':
            return False
        return datetime.utcnow() > self.due_date

    def update_status(self):
        """Call this to sync overdue status before displaying."""
        if self.status != 'returned':
            if datetime.utcnow() > self.due_date:
                self.status = 'overdue'