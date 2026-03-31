
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
    status = request.args.get('status', '')
    if status:
        all_loans = Loan.query.filter_by(status=status).all()
    else:
        all_loans = Loan.query.all()
    if request.headers.get('HX-Request'):
        return render_template('partials/loan_table.html', loans=all_loans)
    return render_template('loans/index.html', loans=all_loans, status=status)

@loans.route('/add', methods=['GET', 'POST'])
def add():
    form = LoanForm()
    form.book_id.choices = [
        (b.id, f'{b.title} ({b.available_copies} available)')
        for b in Book.query.all() if b.is_available
    ]
    form.member_id.choices = [
        (m.id, f'{m.full_name} ({m.student_id})')
        for m in Member.query.all()
    ]
    if form.validate_on_submit():
        loan = Loan(
            book_id=form.book_id.data,
            member_id=form.member_id.data,
            due_date=form.due_date.data,
            borrow_date=datetime.utcnow(),
            status='active'
        )
        db.session.add(loan)
        db.session.commit()
        flash('Loan created successfully.', 'success')
        return redirect(url_for('loans.index'))
    return render_template('loans/form.html', form=form, title='Add Loan')

@loans.route('/<int:id>')
def detail(id):
    loan = Loan.query.get_or_404(id)
    return render_template('loans/detail.html', loan=loan)

@loans.route('/<int:id>/return', methods=['POST'])
def return_book(id):
    loan = Loan.query.get_or_404(id)
    loan.return_date = datetime.utcnow()
    loan.status = 'returned'
    db.session.commit()
    flash('Book returned successfully.', 'success')
    return redirect(url_for('loans.index'))

@loans.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    loan = Loan.query.get_or_404(id)
    db.session.delete(loan)
    db.session.commit()
    flash('Loan deleted successfully.', 'success')
    return redirect(url_for('loans.index'))