import time
import moment
import datetime

from models import User, Course, Session
from flask_login import current_user
from flask_wtf import FlaskForm as Form
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Regexp, ValidationError, Email, Length, EqualTo
from wtforms import TextAreaField, TextField, SubmitField, StringField, PasswordField, SelectField, TimeField

def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User with that name already exists.')

def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')

class SignUpForm(Form):
    username = StringField(
        'Name',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z]+$',
                message=("Name cannot contain symbols or special character")
            ),
            name_exists
        ]
    )
    email  = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=3),
            EqualTo('confirm_password', message='Make sure passwords match correctly.')
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )
    submit = SubmitField("Sign Up")


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


class UpdateAccountForm(Form):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Update')

class CourseForm(Form):
    name = TextField("Name this course")
    description = TextAreaField("Add Description")
    duration = TextField("Add Duration")
    submit = SubmitField('Create Course')

class UserCourseSessionForm(Form):
    user = TextField(),
    course = TextField(),
    sumbit = SubmitField()