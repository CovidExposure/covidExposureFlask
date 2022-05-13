from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import login_user, login_required, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"success": False})
    
    login_user(user, remember=remember)
    return jsonify({"success": True, "user_name": user.name})

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        return jsonify({"success": False, "failure": "user_exists"})

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"success": True})

@login_required
@auth.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({"success": True})
