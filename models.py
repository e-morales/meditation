import datetime
from peewee import *

DATABASE = SqliteDatabase('om.db')
db = DATABASE

class Session(Model):
    name = CharField()
    description = TextField()
    duration = CharField()
    audio = CharField()

    class Meta:
        database = DATABASE


class Course(Model):
    breathe = CharField()
    sleep = CharField()
    stress = CharField()

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
        DATABASE.create_tables([Session, Course], safe=True)
        DATABASE.close()