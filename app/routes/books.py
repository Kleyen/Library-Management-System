from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models.book import Book
from app.forms import BookForm
from sqlalchemy.exc import IntegrityError

books = Blueprint('books', __name__, url_prefix='/books')


@books.route('/')
def index():
    search = request.args.get('search', '').strip()
    if search:
        all_books = Book.query.filter(
            Book.title.ilike(f'%{search}%') |
            Book.author.ilike(f'%{search}%') |
            Book.isbn.ilike(f'%{search}%')
        ).order_by(Book.title).all()
    else:
        all_books = Book.query.order_by(Book.title).all()

    # Return partial for HTMX requests
    if request.headers.get('HX-Request'):
        return render_template('partials/book_table.html', books=all_books)

    return render_template('books/index.html', books=all_books, search=search)


@books.route('/add', methods=['GET', 'POST'])
def add():
    form = BookForm()
    if form.validate_on_submit():
        try:
            book = Book(
                title=form.title.data.strip(),
                author=form.author.data.strip(),
                isbn=form.isbn.data.strip(),
                genre=form.genre.data.strip() if form.genre.data else None,
                published_year=form.published_year.data,
                quantity=form.quantity.data
            )
            db.session.add(book)
            db.session.commit()
            flash('Book added successfully.', 'success')
            return redirect(url_for('books.index'))
        except IntegrityError:
            db.session.rollback()
            flash('A book with that ISBN already exists.', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')

    return render_template('books/form.html', form=form, title='Add Book')


@books.route('/<int:id>')
def detail(id):
    book = Book.query.get_or_404(id)
    return render_template('books/detail.html', book=book)


@books.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    book = Book.query.get_or_404(id)
    form = BookForm(obj=book)
    if form.validate_on_submit():
        try:
            book.title         = form.title.data.strip()
            book.author        = form.author.data.strip()
            book.isbn          = form.isbn.data.strip()
            book.genre         = form.genre.data.strip() if form.genre.data else None
            book.published_year = form.published_year.data
            book.quantity      = form.quantity.data
            db.session.commit()
            flash('Book updated successfully.', 'success')
            return redirect(url_for('books.index'))
        except IntegrityError:
            db.session.rollback()
            flash('A book with that ISBN already exists.', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')

    return render_template('books/form.html', form=form, title='Edit Book')


@books.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    book = Book.query.get_or_404(id)
    try:
        db.session.delete(book)
        db.session.commit()
        flash('Book deleted successfully.', 'success')
    except Exception:
        db.session.rollback()
        flash('Cannot delete this book — it has existing loans.', 'danger')
    return redirect(url_for('books.index'))