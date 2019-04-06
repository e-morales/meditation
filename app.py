from flask import Flask, g
from flask import render_template, flash, redirect, url_for
import json
import models
from forms import SessionForm, PostForm

DEBUG = True 
PORT = 8000

app = Flask(__name__)
app.secret_key = 'poop'


# Handle requests coming in before and when they complete after
@app.before_request
def before_request():
    """Connect to the DB before each request."""
    g.db = models.db
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the DB connection after each request."""
    g.db.close()
    return response


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SessionForm()
    if form.validate_on_submit():
        # if its valid, create a new session
        models.Session.create(name=form.name.data.strip(), description=form.description.data.strip(), duration=form.duration.data.strip(), audio=form.audio.data.strip())

        flash("New Session registered. Called: {}".format(form.name.data))
        #redirect to main Session index
        return redirect('/r')
        #if its not valid then send the user back to the original view 
    return render_template("new_session.html", title="New Session", form=form)


@app.route('/r')
@app.route('/r/<session>')
def r(session=None):
    if session == None:
        sessions = models.Session.select().limit(100)
        return render_template("sessions.html", sessions=sessions)
    else:
        #find the right session
        session_id = int(session)
        session = models.Session.get(models.Session.id == session_id)

    
        #send the found Session to the template
        return render_template("session.html", session=session, posts=posts, form=form)

@app.route('/courses')
@app.route('/courses/<course>')
def courses(course=None):
    if course == None:
        courses = models.Course.select().limit(100)
        return render_template("courses.html", courses=courses)
    else:
        course_id = int(course)
        course = models.Course.get(models.Course.id == course_id)

    return render_template("course.html", course=course)











if __name__ == '__main__':
    # initialize connection to models
    models.initialize()
    app.run(debug=DEBUG, port=PORT)