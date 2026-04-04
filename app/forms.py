from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange


class BookForm(FlaskForm):
    title          = StringField('Title',
                        validators=[DataRequired(), Length(max=200)])
    author         = StringField('Author',
                        validators=[DataRequired(), Length(max=200)])
    isbn           = StringField('ISBN',
                        validators=[DataRequired(), Length(max=20)])
    genre          = StringField('Genre',
                        validators=[Optional(), Length(max=100)])
    published_year = IntegerField('Published Year',
                        validators=[Optional(), NumberRange(min=1000, max=2100)])
    quantity       = IntegerField('Quantity',
                        validators=[DataRequired(), NumberRange(min=1)])


class MemberForm(FlaskForm):
    student_id = StringField('Student ID',
                    validators=[DataRequired(), Length(max=50)])
    full_name  = StringField('Full Name',
                    validators=[DataRequired(), Length(max=200)])
    email      = StringField('Email',
                    validators=[DataRequired(), Email(), Length(max=120)])
    phone      = StringField('Phone',
                    validators=[Optional(), Length(max=20)])
    program    = StringField('Program',
                    validators=[Optional(), Length(max=100)])


class LoanForm(FlaskForm):
    book_id   = SelectField('Book', coerce=int,
                    validators=[DataRequired()])
    member_id = SelectField('Member', coerce=int,
                    validators=[DataRequired()])
    due_date  = DateField('Due Date', format='%Y-%m-%d',
                    validators=[DataRequired()])