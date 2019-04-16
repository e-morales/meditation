import os
import datetime
import time
import moment 
from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

database = SqliteDatabase('om.db')

#connects models to database
class BaseModel(Model):
    class Meta:
        database = database

class User(BaseModel, UserMixin):
    username = CharField(unique=True)
    email = CharField()
    password = CharField(max_length=15)
    admin = BooleanField(default=False)

    @classmethod
    def create_user(cls, username, email, password, admin=False):
        try:
            cls.create(
                username = username,
                email = email,
                password = generate_password_hash(password),
                admin = admin
            )
        except IntegrityError:
            raise

    

class Course(BaseModel):
    name = CharField()
    description = TextField()
    duration = IntegerField()

    @classmethod
    def create_course(cls, name, description, duration):
        try: 
            cls.create(
                name = name,
                description = description,
                duration = duration
            )
        except IntegrityError:
            raise ValueError("Course error")

class Session(BaseModel):
    name = CharField()
    audio = CharField()
    course = ForeignKeyField(User, backref="course")

    @classmethod
    def create_session(cls, name, audio, course):
        try:
            cls.create(
                name = name,
                audio = audio,
                course = course
            )
        except IntegrityError:
            raise

class UserCourseSession(BaseModel):
    user = ForeignKeyField(User, backref="user")
    course = ForeignKeyField(Course, backref="courses")
    # session = ForeignKeyField(Session, backref="sessions")

    @classmethod
    def create_user_session(cls, user, course):
        try:
            cls.create(
                user = user,
                course = course,
                # session = session
            )
        except IntegrityError:
            raise ValueError("course error")


#initialize database connection, create tables, and close out
def initialize():
    database.connect()
    database.create_tables([User, UserCourseSession, Course, Session])
    database.close()