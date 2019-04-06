import datetime
from peewee import *

db = SqliteDatabase('om.db')

class User(Model):
    username = CharField()
    email = CharField()
    password = CharField()
    photo = CharField()
    progress = CharField()
    isAdmin = False

    class Meta:
        database = db

    

class Course(Model):
    name = CharField()
    description = CharField()
    duration = CharField()

    class Meta:
        database = db

    


class Session(Model):
    name = CharField()
    description = TextField()
    duration = TimeField()
    audio = CharField()
    number = IntegerField()
    course = ForeignKeyField(Course, backref='sessions')

    class Meta:
        database = db

    

class UserCourseSession(Model):
    user = ForeignKeyField(User)
    course = ForeignKeyField(Course)
    session = ForeignKeyField(Session)
    current = BooleanField()

    class Meta:
        database = db

   



# Initialize a connection to the database, create a table for the Session model, and close the connection
def initialize():
        db.connect()
        db.create_tables([User, Session, Course, UserCourseSession], safe=True)
        db.close()