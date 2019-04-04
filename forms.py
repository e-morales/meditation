from flask_wtf import FlaskForm as Form   
from wtforms import TextField, TextAreaField, SubmitField

from models import Session

class SessionForm(Form):
    name = TextField("Name this session")
    description = TextAreaField("Add a description for the session here")
    submit = SubmitField("Create Session")    

    
