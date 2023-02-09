"""Models for movie ratings app."""
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()


# Replace this with your code!

class User(db.Model, UserMixin):
    
    __tablename__ = "users"

    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    email = db.Column(db.String, unique=True, nullable = False)
    password = db.Column(db.String, nullable = False)
    
    #has a relationship with ratings
    # uh oh.. theres a love triangle.....

    def __repr__(self):
        return f'<User user_id={self.id} email={self.email}>'

    def __init__(self, email, password):
        self.email = email
        self.password = password


class Movie(db.Model):

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key = True)
    title = db.Column(db.String)
    overview = db.Column(db.Text)
    release_date = db.Column(db.DateTime)
    poster_path = db.Column(db.String)
 
    #has a relationship with ratings
    def __repr__(self):
        return f"<Movie movie_id={self.movie_id} title={self.title}>"

    
    # def create(cls, email, password):
    #      """Create and return a new user."""

    #      return cls(email=email, password=password)

class Rating(db.Model):

    __tablename__= "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key= True)
    score = db.Column(db.Integer)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.movie_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    movie = db.relationship("Movie", backref="ratings",)
    user = db.relationship("User", backref="ratings")

    def __repr__(self):
        return f"<Rating rating_id={self.rating_id} score={self.score}>"

def connect_to_db(flask_app, db_uri=os.environ["POSTGRES_URI"], echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
