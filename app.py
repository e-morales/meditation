import json
import forms
import models

from flask import Flask, g, request
from flask_bcrypt import check_password_hash
from flask import render_template, flash, redirect, url_for, session, escape
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


app = Flask(__name__)
app.secret_key = 'poop'

#login module initialization
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


# handle requests coming in before and when they complete after
@app.before_request
def before_request():
    """Connect to the db before each request."""
    g.db = models.database
    g.db.connect()

@app.after_request
def after_request(response):
    """Connect to the db after each request."""
    g.db.close()
    return response

# Landing page 
@app.route('/')
def index():
    return render_template("landing.html")

# Login
@app.route('/login', methods=['GET', 'POST'])
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
                flash("Log in success", 'success')
                return redirect(url_for('dash'))
            else:
                flash("Email or password are incorrect", 'error')
    return render_template('login.html', form=form)

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out.", 'success')
    return redirect(url_for('index'))


# Sign up
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = forms.SignUpForm()
    if form.validate_on_submit():
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        user = models.User.get(models.User.username == form.username.data)
        login_user(user)
        name = user.username
        print('Yo')
        return redirect(url_for('dash'))
    return render_template('signup.html', form=form)


# Dashboard Route
@app.route('/dash', methods=['GET', 'POST'])
@login_required
def dash():
    form = forms.CourseForm()
    if form.validate_on_submit():
        models.Course.create(name=form.name.data, description=form.description.data, duration=form.duration.data)
        flash("New Course {} Created".format(form.name.data))
        return redirect('/courses')
    return render_template('new_course.html', title="New Course", form=form, courses=courses)


# Courses Route
@app.route('/courses', methods=['GET', 'POST'])
@app.route('/courses/<course>')
@login_required
def courses(course=None):
    form = forms.UserCourseSessionForm()
    if course == None:
        courses = models.Course.select()
        return render_template('courses.html', courses=courses, form=form)
    else:
        course_id = int(course)
        course = models.Course.get(models.Course.id == course_id)
        if form.validate_on_submit():
            models.UserCourseSession.create(
                user = current_user.id,
                course = form.course_id.data

            )

        return render_template("course.html", course=course, form=form)


# Account Route
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    user = models.User.get(current_user.id)
    form = forms.UpdateAccountForm()
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.save()
        flash("Your account has been updated.", 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', form=form)


DEBUG = True
PORT = 8000



if __name__ == '__main__':
    models.initialize()
    
    
        
    app.run(debug=DEBUG, port=PORT)