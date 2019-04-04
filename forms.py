from flask_wtf import FlaskForm as Form   
from wtforms import TextField, TextAreaField, SubmitField

from models import Session

class SessionForm(Form):
    name = TextField("Name this session")
    description = TextAreaField("Add a description for the session here")
    duration = TextField("The session is this many minutes")
    audio = TextField("The audio is slappin'")
    submit = SubmitField("Create Session")


class PostForm(Form):
    user = TextField("By:")
    title = TextField("Title")
    text = TextAreaField("Content")
    submit = SubmitField('Create Post') 



    
