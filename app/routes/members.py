
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models.member import Member
from app.forms import MemberForm

members = Blueprint('members', __name__, url_prefix='/members')

@members.route('/')
def index():
    search = request.args.get('search', '')
    if search:
        all_members = Member.query.filter(
            Member.full_name.ilike(f'%{search}%') |
            Member.student_id.ilike(f'%{search}%') |
            Member.email.ilike(f'%{search}%')
        ).all()
    else:
        all_members = Member.query.all()
    if request.headers.get('HX-Request'):
        return render_template('partials/member_table.html', members=all_members)
    return render_template('members/index.html', members=all_members, search=search)

@members.route('/add', methods=['GET', 'POST'])
def add():
    form = MemberForm()
    if form.validate_on_submit():
        try:
            member = Member(
                student_id=form.student_id.data,
                full_name=form.full_name.data,
                email=form.email.data,
                phone=form.phone.data,
                program=form.program.data
            )
            db.session.add(member)
            db.session.commit()
            flash('Member added successfully.', 'success')
            return redirect(url_for('members.index'))
        except Exception:
            db.session.rollback()
            flash('Error: Student ID or Email already exists.', 'danger')
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
        form.populate_obj(member)
        db.session.commit()
        flash('Member updated successfully.', 'success')
        return redirect(url_for('members.index'))
    return render_template('members/form.html', form=form, title='Edit Member')

@members.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    member = Member.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    flash('Member deleted successfully.', 'success')
    return redirect(url_for('members.index'))