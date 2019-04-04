import datetime
from peewee import *

DATABASE = SqliteDatabase('om.db')
db = DATABASE


class User(Model):
    username = CharField()
    email = CharField()
    password = CharField()
    photo = CharField()
    progress = CharField()
    isAdmin = False

    class Meta:
        database = DATABASE

class Course(Model):
    name = CharField()
    description = CharField()
    duration = CharField()

    class Meta:
        database = DATABASE


class Session(Model):
    name = CharField()
    description = TextField()
    duration = TimeField()
    audio = CharField()
    number = IntegerField()
    course = ForeignKeyField(Course, backref='sessions')

    class Meta:
        database = DATABASE

class UserCourseSession(Model):
    user = ForeignKeyField(User)
    course = ForeignKeyField(Course)
    session = ForeignKeyField(Session)
    current = BooleanField()

    class Meta:
        database = DATABASE


# class Post(Model):
#     timestamp = DateTimeField(default=datetime.datetime.now)
#     user = CharField()
#     title = CharField()
#     text = TextField()
#     # relate the post model to the session model
#     session = ForeignKeyField(Session, backref="posts")
    
#     class Meta:
#         database = DATABASE
#         order_by = ('-timestamp',)






# Initialize a connection to the database, create a table for the Session model, and close the connection
def initialize():
        DATABASE.connect()
        DATABASE.create_tables([User, Session, Course, UserCourseSession], safe=True)
        DATABASE.close()