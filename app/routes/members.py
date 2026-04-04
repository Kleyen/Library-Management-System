from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models.member import Member
from app.forms import MemberForm
from sqlalchemy.exc import IntegrityError

members = Blueprint('members', __name__, url_prefix='/members')


@members.route('/')
def index():
    search = request.args.get('search', '').strip()
    if search:
        all_members = Member.query.filter(
            Member.full_name.ilike(f'%{search}%') |
            Member.student_id.ilike(f'%{search}%') |
            Member.email.ilike(f'%{search}%')
        ).order_by(Member.full_name).all()
    else:
        all_members = Member.query.order_by(Member.full_name).all()

    # Return partial for HTMX requests
    if request.headers.get('HX-Request'):
        return render_template('partials/member_table.html', members=all_members)

    return render_template('members/index.html',
                           members=all_members, search=search)


@members.route('/add', methods=['GET', 'POST'])
def add():
    form = MemberForm()
    if form.validate_on_submit():
        try:
            member = Member(
                student_id=form.student_id.data.strip(),
                full_name=form.full_name.data.strip(),
                email=form.email.data.strip(),
                phone=form.phone.data.strip() if form.phone.data else None,
                program=form.program.data.strip() if form.program.data else None
            )
            db.session.add(member)
            db.session.commit()
            flash('Member added successfully.', 'success')
            return redirect(url_for('members.index'))
        except IntegrityError:
            db.session.rollback()
            flash('A member with that Student ID or Email already exists.',
                  'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')

    return render_template('members/form.html', form=form, title='Add Member')


@members.route('/<int:id>')
def detail(id):
    member = Member.query.get_or_404(id)
    return render_template('members/detail.html', member=member)


@members.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    member = Member.query.get_or_404(id)
    form = MemberForm(obj=member)
    if form.validate_on_submit():
        try:
            member.student_id = form.student_id.data.strip()
            member.full_name  = form.full_name.data.strip()
            member.email      = form.email.data.strip()
            member.phone      = form.phone.data.strip() if form.phone.data else None
            member.program    = form.program.data.strip() if form.program.data else None
            db.session.commit()
            flash('Member updated successfully.', 'success')
            return redirect(url_for('members.index'))
        except IntegrityError:
            db.session.rollback()
            flash('A member with that Student ID or Email already exists.',
                  'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')

    return render_template('members/form.html', form=form, title='Edit Member')


@members.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    member = Member.query.get_or_404(id)
    try:
        db.session.delete(member)
        db.session.commit()
        flash('Member deleted successfully.', 'success')
    except Exception:
        db.session.rollback()
        flash('Cannot delete this member — they have existing loans.', 'danger')
    return redirect(url_for('members.index'))