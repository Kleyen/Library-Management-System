from flask import Blueprint, render_template
from app.models.book import Book
from app.models.member import Member
from app.models.loan import Loan

main = Blueprint('main', __name__)


@main.route('/')
def dashboard():
    try:
        total_books   = Book.query.count()
        total_members = Member.query.count()
        active_loans  = Loan.query.filter_by(status='active').count()
        overdue_loans = Loan.query.filter_by(status='overdue').count()
        recent_loans  = Loan.query.order_by(
                            Loan.borrow_date.desc()).limit(5).all()
    except Exception:
        total_books   = 0
        total_members = 0
        active_loans  = 0
        overdue_loans = 0
        recent_loans  = []

    return render_template('dashboard.html',
        total_books=total_books,
        total_members=total_members,
        active_loans=active_loans,
        overdue_loans=overdue_loans,
        recent_loans=recent_loans
    )