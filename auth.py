# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db
import os
from app import app

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = db.query(User).filter_by(email=email).first()

 
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login credentials and try again.')
        return redirect(url_for('auth.login'))  # if user doesn't exist or password is wrong, reload the page

    login_user(user, remember=remember)
    flash('You have been logged in.')
    return redirect(url_for('main.drive'))


@auth.route('/register')
def signup():
    return render_template("register.html")


@auth.route('/register', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = db.query(User).filter_by(email=email).first()  # if this returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.register'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.add(new_user)
    db.commit()

    user_space = os.makedirs(app.config['UPLOAD_FOLDER'] + "/" + str(new_user.id))


    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
