from flask import Flask, g
from flask import render_template, flash, redirect, url_for, session, escape
import json
import models
from config import Config
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
import forms
from flask_bcrypt import check_password_hash

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
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/admin')
def admin():
    return render_template("admin.html")

##### ==++= Registration ======
@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
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
            return redirect(url_for('home'))

    # else:
    #     flash("Hello, new student.", 'success')
    #     models.User.create_user(
    #         username=form.username.data,
    #         email=form.email.data,
    #         password=form.password.data
    #     )
    #     return redirect(url_for('courses'))
    return render_template('register.html', form=form)

def admin_user():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        if "mount.olympus" in form.email.data:
            flash("Registered as an instructor", 'success')
            models.User.create_user(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data        
            )
        return redirect(url_for('admin'))



## login 
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
                return redirect(url_for('home'))
            else: 
                flash("Email or password are incorrect", 'error')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out", "success")
    return redirect(url_for('home'))



@app.route('/courses')
def courses():
    return render_template("courses.html")



@app.route('/sessions', methods=['GET', 'POST'])
def sessions():
        #if its not valid then send the user back to the original view 
    return render_template("sessions.html", title="New Session")




if __name__ == '__main__':
    # initialize connection to models
    models.initialize()
    try:
        models.User.create_user(
            username='enrique',
            email="enrique@enrique.com",
            password='password'
        ),
        models.Course.create_course(
            name = "Chill Vibes",
            description = "Chill",
            duration = "One hour",
            progress = "Nice",
            user = 1
        )
    except ValueError:
        pass

app.run(debug=True, port=PORT)