"""Server for movie ratings app."""


from flask import Flask, render_template, session, url_for, redirect, flash, session, request
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
    movies = Movie.get_movies()
    ratings = Rating.all_ratings()
    if current_user.is_authenticated:
        user_email = User.split_email(current_user)
        return render_template('base.html', movies = movies, ratings= ratings, user= user_email[0])
    else:
        return render_template('base.html', movies = movies)

@app.route('/movies')
@login_required
def all_movies():
    user_email = User.split_email(current_user)
    movies = Movie.get_movies()
    return render_template('all_movies.html', movies = movies, user=user_email[0])

@app.route('/movies/<movie_id>', methods=['GET', 'POST'])
@login_required
def movie_deets(movie_id):
    rating_form = RatingForm()
    moviee = Movie.query.filter_by(movie_id = movie_id).first()
    mov = moviee.movie_id
    user = current_user.id
    user_email = User.split_email(current_user)
    # if current_user != None:
    #     return redirect(url_for('home'))
    if rating_form.validate_on_submit():
        score = int(rating_form.rating.data)
        new_rating = Rating.create_rating(score, mov, user)
        db.session.add(new_rating)
        db.session.commit()
        flash(f'you gave {moviee.title} a rating of {score} out of 5')
    return render_template('movie_deets.html', moviee=moviee, rating_form = rating_form, user = user_email[0])

@app.route('/users')
@login_required
def all_users():
    all_users = User.get_users()
    users = []
    for you in all_users:
        split_users = you.email.split('@')
        users.append(split_users)
        
        

    user_email = User.split_email(current_user)
    return render_template('users.html', users = users, user = user_email[0])

@app.route('/users/<user_id>')
@login_required
def user_profile(user_id):
    user = User.query.filter_by(id = user_id).first()
    rating = Rating.query.filter_by(user_id = user_id).all()
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
            new_user = User.create_user(email, password)
            db.session.add(new_user)
            db.session.commit()
            flash(f'{new_user.email} has been created!')
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
                return redirect(url_for('home')), flash('logged in')
        return 'wrong password or email'
    else:
        return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.errorhandler(404)
def error(e):
    flash('Hey sorry the page you are looking for is unavailable right now, sign in to get access to an unlimited amount of movies!')
    return render_template('401.html')

@app.errorhandler(401)
def error(e):
    flash('Hey sorry the page you are looking for is unavailable right now, sign in to get access to an unlimited amount of movies!')
    return render_template('401.html')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="localhost", port = 3001, debug=True)
