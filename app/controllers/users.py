from flask import render_template, redirect, request, session, flash
from app.models.user import User
from app.models.message import Message
from app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

#index
@app.route('/')
def index():
    return render_template('index.html')


#hidden route for registration form
@app.route('/register', methods=['POST'])
def register():
    isValid = User.validate_registration(request.form)
    if not isValid:
        return redirect('/')
    newUser = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        #hash password
        'password' : bcrypt.generate_password_hash(request.form['password']),
    }
    id = User.insert(newUser)
    if not id:
        flash('Something went wrong.')
        return redirect('/')
    session['user_id'] = id
    flash('You are logged in.')
    return redirect('/dashboard/')


#hidden route from login form
@app.route('/login', methods=['POST'])
def login():
    data = {
        'email' : request.form['email']
    }
    user = User.get_email(data)
    if not user:
        flash('That email is not in our database. Please register.')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Wrong password.')
        return redirect('/')
    session['user_id'] = user.id
    flash('You are logged in.')
    return redirect('/dashboard/')

#view page after login successfully
@app.route('/dashboard/')
def wall():
    if 'user_id' not in session:
        flash('You must be logged in to view this page.')
        return redirect('/')
    data = {
        'id' : session['user_id']
    }
    results = User.get_all()
    messages = Message.get_user_messages(data)
    return render_template('wall.html', userList = results, user=User.get_one(data), messages = messages)

#logout hidden method, redirect back to index login page.
@app.route('/logout')
def logout():
    session.clear()
    # flash('You are now logged out.')
    return redirect('/')