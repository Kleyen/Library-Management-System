from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models.loan import Loan
from app.models.book import Book
from app.models.member import Member
from app.forms import LoanForm
from datetime import datetime

loans = Blueprint('loans', __name__, url_prefix='/loans')


@loans.route('/')
def index():
    status = request.args.get('status', '').strip()
    if status in ('active', 'returned', 'overdue'):
        all_loans = Loan.query.filter_by(status=status)\
                       .order_by(Loan.borrow_date.desc()).all()
    else:
        all_loans = Loan.query.order_by(Loan.borrow_date.desc()).all()

    # Return partial for HTMX requests
    if request.headers.get('HX-Request'):
        return render_template('partials/loan_table.html', loans=all_loans)

    return render_template('loans/index.html', loans=all_loans, status=status)


@loans.route('/add', methods=['GET', 'POST'])
def add():
    form = LoanForm()

    # Populate dropdowns
    available_books = Book.query.order_by(Book.title).all()
    all_members     = Member.query.order_by(Member.full_name).all()

    form.book_id.choices = [
        (b.id, f'{b.title} — {b.author} ({b.available_copies} available)')
        for b in available_books if b.is_available
    ]
    form.member_id.choices = [
        (m.id, f'{m.full_name} ({m.student_id})')
        for m in all_members
    ]

    # No available books — block form
    if not form.book_id.choices:
        flash('No books are currently available for loan.', 'warning')
        return redirect(url_for('loans.index'))

    if form.validate_on_submit():
        # Validate due date is in the future
        if form.due_date.data <= datetime.utcnow().date():
            flash('Due date must be a future date.', 'danger')
            return render_template('loans/form.html', form=form, title='Add Loan')
        try:
            loan = Loan(
                book_id=form.book_id.data,
                member_id=form.member_id.data,
                due_date=datetime.combine(form.due_date.data,
                                          datetime.min.time()),
                borrow_date=datetime.utcnow(),
                status='active'
            )
            db.session.add(loan)
            db.session.commit()
            flash('Loan created successfully.', 'success')
            return redirect(url_for('loans.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')

    return render_template('loans/form.html', form=form, title='Add Loan')


@loans.route('/<int:id>')
def detail(id):
    loan = Loan.query.get_or_404(id)
    return render_template('loans/detail.html', loan=loan)


@loans.route('/<int:id>/return', methods=['POST'])
def return_book(id):
    loan = Loan.query.get_or_404(id)
    if loan.status == 'returned':
        flash('This book has already been returned.', 'warning')
        return redirect(url_for('loans.index'))
    try:
        loan.return_date = datetime.utcnow()
        loan.status      = 'returned'
        db.session.commit()
        flash('Book returned successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred: {str(e)}', 'danger')
    return redirect(url_for('loans.index'))


@loans.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    loan = Loan.query.get_or_404(id)
    try:
        db.session.delete(loan)
        db.session.commit()
        flash('Loan deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred: {str(e)}', 'danger')
    return redirect(url_for('loans.index'))