"""Server for movie ratings app."""

import crud
from flask import Flask, render_template, session, url_for, redirect, flash, session
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from datetime import timedelta

from forms import LoginForm, RegisterForm, RatingForm
from model import connect_to_db, User, Movie, Rating, db

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'dev'

login_manager = LoginManager()
login_manager.init_app(app)

app.jinja_env.undefined = StrictUndefined



# Replace this with routes and view functions!

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/movies')
@login_required
def all_movies():
    movies = Movie.query.all()
    return render_template('all_movies.html', movies = movies)

@app.route('/movies/<movie_id>', methods=['GET', 'POST'])
@login_required
def movie_deets(movie_id):
    rating_form = RatingForm()
    rating = rating_form.rating.data
    moviee = Movie.query.filter_by(movie_id = movie_id).first()
    user = User.query.filter_by(id= movie_id).first()
    if rating_form.validate_on_submit():
        new_rating = crud.create_rating(user, moviee, rating)
        db.session.add(new_rating)
        db.session.commit()
    return render_template('movie_deets.html', moviee=moviee, rating_form = rating_form, )

@app.route('/users')
@login_required
def all_users():
    users = User.query.all()
    return render_template('users.html', users = users)

@app.route('/users/<user_id>')
@login_required
def user_profile(user_id):
    user = User.query.filter_by(id = user_id).first()
    rating = Rating.query.filter_by(user_id = user_id).first()
    return render_template('user_profile.html', user = user, rating = rating)

@app.route('/register', methods =['GET' ,'POST'])
def register_email():
    register = RegisterForm()
    email = register.email.data
    password = register.password.data
    password_confirmed = register.password_confirmed.data

    e = User.query.filter_by(email =email).first()
    if register.validate_on_submit():
        if e:
            flash('email already exists')
            return redirect('/register')
        if password != password_confirmed:
            return 'passwords do not match'
        else:
            new_user = crud.create_user(email, password)
            db.session.add(new_user)
            db.session.commit()
            flash('{new_user.email} has been created!')
            return redirect(url_for('home'))
    return render_template('register.html', register = register)
    

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id = user_id).first()


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data

        user = User.query.filter_by(email=email).first()
        
        if user: 
            if user.password == password:
                login_user(user, remember = remember_me, duration = timedelta(days = 7))
                return redirect(url_for('home'))
        return 'wrong password or email'
    else:
        return render_template('login.html', form = form)


@app.errorhandler(401)
def error(e):
    flash('Hey sorry the page you are looking for is unavailable right now, sign in to get access to an unlimited amount of movies!')
    return render_template('401.html')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="localhost", port = 3001, debug=True)
