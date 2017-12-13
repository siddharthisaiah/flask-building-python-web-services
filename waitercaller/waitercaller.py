from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from mockdbhelper import MockDBHelper as DBHelper
from user import User


DB = DBHelper()
app = Flask(__name__)
app.secret_key = 't2CNVBVfXZw3viLkBe8tOkgABDhaFsnpo/WE8xdzDOK9S2wIgNeYbeyDGR177c+MR3AyQakKuNSLJGWdcqaH/31F83GOHDz0mxR'
login_manager = LoginManager(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/account")
@login_required
def account():
    return "You are logged in"


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user_password = DB.get_user(email)
    if user_password and user_password == password:
        user = User(email)
        login_user(user, remember=True)
        return redirect(url_for('account'))
    return home()


@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
