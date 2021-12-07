"""
app.py
Jamie Shearer
CS 166 / Fall 2021

A program that takes a username and password and then allows the user to
access different things based on their credentials. Usernames and passwords are
stored in an SQL database. Passwords are hashed and salted
"""

from helpers import *
# from config import display
from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__, static_folder='instance/static')

app.config.from_object('config')


@app.route("/", methods=['GET', 'POST'])
def home():
    """ Home page """
    return render_template('home.html',
                           title="Home Page",
                           heading="Home Page"
                           # show=display
                           )


@app.route("/login", methods=['GET', 'POST'])
def login():
    """ Log the user in """
    if request.method == 'POST':
        # User-entered values
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            # stored = credentials[username]['pw_hash']
            stored_data = query_db()

            if sign_in(stored_data, username, password):
                print("Logged in!")
                for user in stored_data:
                    if user[0] == username:
                        access_level = user[2]
                return redirect(url_for('login_success', id_=access_level))
        except KeyError:
            pass
        flash("Invalid username or password!", 'alert-danger')
    return render_template('login.html',
                           title="Secure Login",
                           heading="Secure Login")


@app.route("/login_success/<int:id_>", methods=['GET', 'POST'])
def login_success(id_):
    # TODO: Different home pages for people with different access levels
    flash("Welcome! You have logged in!", 'alert-success')
    return render_template('customer_home.html',
                           title="Customer Home",
                           heading="Customer Home")


@app.route("/new-user", methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        # User-entered values
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            success = add_user(username, password)    # TODO: This currently sets everyone's access level to 1

            if not success:
                flash("A user with that username is already registered! Try again!", 'alert-danger')
            else:
                flash("Success!", 'alert-success')

        except KeyError:
            pass

    return render_template('new_user.html',
                           title="Register New User",
                           heading="register New User")
