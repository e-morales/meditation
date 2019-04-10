from flask_wtf import FlaskForm as Form   
from wtforms import TextField, TextAreaField, SubmitField, StringField, PasswordField, SelectField, TimeField
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from models import User
import datetime
import moment
import time
from wtforms.validators import DataRequired, Regexp, ValidationError, Email, Length, EqualTo


def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User with that name already exists.')

def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')


class RegisterForm(Form):
    username = StringField(
        'Name',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z]+$',
                message=("Name cannot contain symbols or special characters")
            ),
            name_exists
        ]
    )
    email = StringField(
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

    submit = SubmitField('submit')


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('submit')




class UpdateAccountForm(Form):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Update')





# class SessionForm(Form):
#     name = TextField("Name this session")
#     description = TextAreaField("Add a description for the session here")
#     duration = TextField("The session is this many minutes")
#     audio = TextField("The audio is slappin'")
#     submit = SubmitField("Create Session")


# class PostForm(Form):
#     user = TextField("By:")
#     title = TextField("Title")
#     text = TextAreaField("Content")
#     submit = SubmitField('Create Post') 



    
