from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SelectField, SubmitField, validators, BooleanField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Length

class LoginForm(FlaskForm)
    email = StringField("Enter your email", [validators.InputRequired()])
    password= StringField("Password here", [validators.InputRequired()])

