import os
import datetime
import time
import moment 
from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = SqliteDatabase('om.db', pragmas={'foreign_keys': 1})

class User(UserMixin, Model):
    username = CharField(unique=True, null=False)
    email = CharField(unique=True, null=False)
    password = CharField(max_length=25)

    class Meta:
        database = DATABASE
        db_table = 'user'

    @classmethod
    def create_user(cls, username, email, password):
        try:
            cls.create(
                username = username,
                email = email,
                password = generate_password_hash(password) 
            )
        except IntegrityError:
            raise

    @classmethod
    def get_courses(self):
        return Course.select().where(Course.user == self)

    
class Course(Model):
    name = CharField()
    description = CharField()
    duration = CharField()
    user = ForeignKeyField(User, backref="courses")

    class Meta:
        database = DATABASE
        db_table = 'course'

    @classmethod
    def create_course(cls, name, description, duration, user):
        try:
            cls.create(
                name = name,
                description = description,
                duration = duration,
                user=user
            )
        except IntegrityError:
            raise ValueError("course error")

class Session(Course):
    name = CharField()
    description = TextField()
    audio = CharField()
    course = ForeignKeyField(Course, backref='course')
    class Meta:
        database = DATABASE
        db_table = 'session'
    
    @classmethod
    def create_session(cls, name, description, audio, course):
        try:
            cls.create(
                name = name,
                description = description,
                audio = audio,
                course=course
            )
        except IntegrityError:
            raise

class UserCourseSession(Model):
    user = ForeignKeyField(User, backref="user")
    course = ForeignKeyField(Course, backref="courses")
    session = ForeignKeyField(Session, backref="sessions")

    class Meta:
        database = DATABASE
        db_table = 'user_course_session'

    @classmethod
    def create_user_session(cls, user, course, session):
        try:
            cls.create(
                user = user,
                course=course,
                session = session
            )
        except IntegrityError:
            raise ValueError("course error")

# Initialize a connection to the database, create a table for the Session model, and close the connection
def initialize():
        DATABASE.connect()
        DATABASE.create_tables([User, Course, Session, UserCourseSession], safe=True)
        DATABASE.close()