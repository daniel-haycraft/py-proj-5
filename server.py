"""Server for movie ratings app."""

from flask import Flask, render_template
from flask_login import LoginManager, current_user, login_user, logout_user

login_manager = LoginManager()

app = Flask(__name__)

app.secret_key = 'secret'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = email.form.data
        password = password.form.data
        remember_me = remember_me.form.data

        user = User.query.filter_by(email= email).first()
        
        if user.password != password:
            login_user(user)
            return redirect(url_for())
        else:
            return "wrong password or email"
    return render_template('login.html', form = form)
        
# Replace this with routes and view functions!


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="localhost", port = 3001, debug=True)
