from app.extensions import db
from datetime import datetime


class Member(db.Model):
    __tablename__ = 'members'

    # Primary Key
    id         = db.Column(db.Integer, primary_key=True)

    # Fields - edit values as needed
    student_id = db.Column(db.String(50), unique=True, nullable=False)
    full_name  = db.Column(db.String(200), nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    phone      = db.Column(db.String(20), nullable=True)
    program    = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to loans table
    loans = db.relationship('Loan', backref='member', lazy=True)

    def __repr__(self):
        return f'<Member {self.full_name}>'

    # ------------------------------------------------------- #
    # ------------------------------------------------------- #

    @property
    def active_loans(self):
        return [loan for loan in self.loans if loan.status == 'active']

    @property
    def has_overdue(self):
        return any(loan.status == 'overdue' for loan in self.loans)