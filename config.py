import os

class Config(object):
    SECRET_KEY = 'poop'

    def __repr__(self):
        return (f'<Secret key is {self.SECRET_KEY}')