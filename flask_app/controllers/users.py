from flask import render_template,request,redirect, session, flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user import User

@app.route('/insert_user', methods=["POST"])
def insert_registration():
    data = {
        'user_name': request.form['user_name'],
        'password': request.form['password'],
        'password2': request.form['password2'],
    }
    if User.verify_user(data): # if true (or truthy), this user_name already exists
        flash('Username already taken. Try a different username.')
        return redirect('/login')
    if not User.validate_registration(data):
        return redirect('/login')
    data['password'] = bcrypt.generate_password_hash(data['password'])
    User.insert_user(data)
    return redirect('/game')

@app.route("/login")
def register_login():
    return render_template("login.html")

@app.route('/login', methods=["POST"])
def login():
    data = { 'user_name': request.form['user_name'], 'password': request.form['password'] }
    user = User.verify_user(data)
    if not user:
      flash("Invalid Username/Password")
      return redirect('/login')
    if not bcrypt.check_password_hash(user['password'], data['password']):
      flash("Invalid Username/Password")
      return redirect('/login')
    User.to_session(user)
    return redirect('/game')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')



