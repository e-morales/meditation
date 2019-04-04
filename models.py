import datetime
from peewee import *

DATABASE = SqliteDatabase('om.db')
db = DATABASE

class Session(Model):
    name = CharField()
    description = TextField()

    class Meta:
        database = DATABASE






















# Initialize a connection to the database, create a table for the Session model, and close the connection
def initialize():
        DATABASE.connect()
        DATABASE.create_tables([Session], safe=True)
        DATABASE.close()