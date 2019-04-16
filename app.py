import json
import forms
import models

from config import Config
from flask_wtf import FlaskForm
from flask import Flask, g, request
from flask_bcrypt import check_password_hash
from flask import render_template, flash, redirect, url_for, session, escape
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

DEBUG = True
PORT = 8000

app = Flask(__name__)
app.config.from_object(Config)

# login manager module initialization
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

# Handle requests coming in before and when they complete after
@app.before_request
def before_request():
    """Connect to the DB before each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):
    """Close the DB connection after each request."""
    g.db.close()
    return response


@app.route('/')
def index():
    return render_template("landing.html")


@app.route('/home')
@login_required
def dash():
    courses = models.UserCourseSession.select(models.Course).join(models.Course).where(models.UserCourseSession.user==current_user.id)
    # print(courses)
    # for course in courses:
    #     print(course.course.id)
    #     sessions = models.UserCourseSession.select(models.Session).join(models.Session).where(models.UserCourseSession.user==current_user.id, models.Session.course==course.course.id)
    #     # for session in sessions:
    #         # print(session.session.id)
    #     course.sessions = sessions
        
    return render_template('dash.html', courses=courses, sessions=sessions)



##### ===== SignUp ======
@app.route('/signup', methods=('GET', 'POST'))
def signup():
    form = forms.SignUpForm()
    if form.validate_on_submit():
            models.User.create_user(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data        
            )
            user = models.User.get(models.User.username == form.username.data)
            login_user(user)
            name = user.username
            print('hello')
            return redirect(url_for('dash'))

    return render_template('signup.html', form=form)


## Login 
@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Email or password are incorrect", 'error')
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("Log in success",'success')
                return redirect(url_for('dash'))
            else: 
                flash("Email or password are incorrect", 'error')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out", "success")
    return redirect(url_for('dash'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    user = models.User.get(current_user.id)
    form = forms.UpdateAccountForm()
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.save()
        flash('Your account is updated', 'success')
        return redirect(url_for('account'))
    elif request.method =='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


@app.route('/courses', methods=['GET', 'POST'])
@login_required
def courses():
    courses = models.Course.select()
    return render_template("courses.html", courses=courses)

@app.route('/courses/<courseid>', methods=['GET', 'POST'])
@login_required
def add_course(courseid=None):
    courses = models.UserCourseSession.select().where(models.UserCourseSession.user==current_user.id, models.UserCourseSession.course==courseid).get()
    # if course_present == None:
    # courses = models.UserCourseSession.select()

    
    return render_template("dash.html", courses=courses)


@app.route('/sessions', methods=['GET', 'POST'])
@login_required
def sessions():

    sessions = models.Session.select()
    return render_template("sessions.html")

@app.route('/sessions/<course_id>')
@login_required
def get_sessions(course_id):
    print('in route')
    courses = models.UserCourseSession.select(models.Course).join(models.Course).where(models.UserCourseSession.user==current_user.id)
    sessions = models.UserCourseSession.select(models.Session).join(models.Session).where(models.UserCourseSession.user==current_user.id, models.UserCourseSession.course==course_id)
    print(sessions)
    # for course in courses:
    #     print(course.session.audio)
    return render_template('dash.html', courses=courses, sessions=sessions)

if __name__ == '__main__':
    # initialize connection to models
    models.initialize()
    try:
    #     models.User.create_user(
    #         username='enrique',
    #         email="enrique@enrique.com",
    #         password='password'
    #     )
        models.Course.create_course(
            name = "Relax",
            description = "Relaxation Techniques",
            duration = "10 mins",
            user = 1
        )
    #     models.Course.create_course(
    #         name = "Stress",
    #         description = "Stress Relieving  Techniques",
    #         duration = "10 mins",
    #         progress = "0%",
    #         user = 1
    #     )
    #     models.Course.create_course(
    #         name = "Sleep",
    #         description = "Deep Sleep Techniques",
    #         duration = "10 mins",
    #         progress = "0%",
    #         user = 1
    #     )
    #     models.Session.create_session(
    #         name = "Session 1",
    #         description = "This is the first session",
    #         number = 1,
    #         duration = 10,
    #         audio = "this is sound",
    #         course = 1,
    #     )
    #     models.Session.create_session(
    #         name = "Session 2",
    #         description = "This is the first session",
    #         number = 1,
    #         duration = 10,
    #         audio = "this is sound",
    #         course = 1,
    #     )
        

    except ValueError:
        pass

app.run(debug=True, port=PORT)