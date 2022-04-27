from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_app.models.project import Project
from flask_bcrypt import Bcrypt
import re
bcrypt = Bcrypt(app)


#Index Page
@app.route('/')
def index():
    return render_template('index.html')


#Register User
@app.route('/user/register', methods= ['POST'])
def register_user():
    is_valid = User.validate_user(request.form)

    if not is_valid:
        return redirect ('/')

    data= {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form["password"]),
    }

    user_id=User.save_user(data)
    if not id:
        flash ("Email already taken")
        return redirect ('/')
    session['user_id']= user_id
    return redirect ('/dashboard')


#Login User
@app.route("/user/login",methods=['POST'])
def login():
    data = {
        "email": request.form['email']
    }
    user = User.get_by_email(data)

    if not user:
        flash("Invalid Email and Password! Who are you?")
        return redirect("/")

    if not bcrypt.check_password_hash(user.password,request.form['password']):
        flash("That's not your password!")
        return redirect("/")
    session['user_id'] = user.id
    return redirect('/dashboard')


#Homepage
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect ('/')

    data = {
        'id': session ['user_id']
    }
    projects = Project.get_all_projects_with_users()
    user = User.get_one_user(data)
    return render_template('dashboard.html', projects=projects, user=user)


#Logout user
@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/')


