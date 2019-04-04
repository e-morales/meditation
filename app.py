from flask import Flask, g
from flask import render_template, flash, redirect, url_for
import json
import models
from forms import SessionForm

DEBUG = True 
PORT = 8000

app = Flask(__name__)
app.secret_key = 'poop'


# Handle requests coming in before and when they complete after
@app.before_request
def before_request():
    """Connect to the DB before each request."""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the DB connection after each request."""
    g.db.close()
    return response


@app.route('/')
def index():
    form = SessionForm()
    return render_template("new_session.html", title="New Session", form=form)

@app.route('/sessions')
@app.route('/sessions/<session>')
def sessions(session=None):
    with open('sessions.json') as json_data:
            sessions = json.load(json_data)
            if session == None:
                return render_template('sessions.html', sessions=sessions)
            else:
                session_id = int(session)
                return render_template('session.html', session=sessions[session_id])









if __name__ == '__main__':
    # initialize connection to models
    models.initialize()
    app.run(debug=DEBUG, port=PORT)