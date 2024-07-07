import ssl

from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import random, smtplib

user_number = {}

auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                r = str(random.randint(100000,999999))
                sender = 'coolvdi1@gmail.com'
                receivers = [email]
                msg = f"""
                From: From Person coolvdi1@gmail.com
                To: To Person {email}
                Subject: 2fa
                number - {r}
                """
                with smtplib.SMTP_SSL("smtp.gmail.com",465,context=ssl.create_default_context()) as server:
                    server.login("coolvdi1@gmail.com", "xuwfzfuqbsfcphfo")
                    server.sendmail(sender,receivers,msg)
                user_number[str(user)] = r
                return redirect(url_for('auth.two_factor_auth' , user = user, email = email))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/two_factor_auth', methods=['GET','POST'])
def two_factor_auth():
    if request.method == 'POST':
        number = request.form.get('number')
        user = request.args['user']
        if user_number[user] == number:
            user_number.pop(user)
            user1 = User.query.filter_by(email=request.args["email"]).first()
            login_user(user1, remember=True)
            return redirect(url_for("views.home"))
    return render_template('two_factor_auth.html', user=current_user)


@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists", category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)

            flash('Account created!', category='success')
            return redirect(url_for('views.home'))


    return render_template("signup.html",user=current_user)
