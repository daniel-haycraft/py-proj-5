
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SelectField, SubmitField, validators, BooleanField, TextAreaField, RadioField
from wtforms.validators import DataRequired, InputRequired, Length

class LoginForm(FlaskForm):
    email = StringField("Enter your email", [validators.InputRequired()])
    password= StringField("Password here", [validators.InputRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    email = StringField("Enter your email", [validators.InputRequired()])
    password= StringField("Password here", [validators.InputRequired()])
    password_confirmed = StringField('Password Again', [validators.InputRequired()])
    submit = SubmitField('Submit')

# first i will write a form that has choices 1-5 
# it would be a radio field
# after user sign in they are able to go in to movies tab and select a movie and be able to rate it! and be send to the db! so ill need to create a function in crud to add a rating if there isn't one
class RatingForm(FlaskForm):
    rating = RadioField('ratings', [validators.InputRequired()], choices = [('1', '1'), ('2', '2'), ('3','3'), ('4','4'), ('5','5')])
    submit = SubmitField('Submit')
