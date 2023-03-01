import flask
import os
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import logging
import requests
from search import search_song
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user, login_user, UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# each user of the app need their secret key #in .env as SECRET_KEY
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# will be done in the later sprints

# database boilerplate code
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + \
    os.path.join(basedir, 'database.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# user loader
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# database models
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256))
    username = db.Column(db.String(16))
    password = db.Column(db.String(16))
    created_playlists = db.Column(db.String(1024))
    playlists_shared_with = db.Column(db.String(1024))
    followers = db.Column(db.String(1024))
    playlists = db.relationship("Playlists", back_populates="user")

# define the get_id method for Flask-Login
    def get_id(self):
        return self.id

class Playlists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    password = db.Column(db.String(16))
    songs = db.Column(db.String(10000))
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    listeners_shared_to = db.Column(db.String(1024))
    user = db.relationship("Users", back_populates="playlists")

with app.app_context():
    db.create_all()

# displaying the Users and Playlist model
@app.route('/UsersAndPlaylist')
def UsersAndPlaylist():
    users = Users.query.all()
    playlists = Playlists.query.all()
    return render_template("UsersAndPlaylist.html", users=users, playlists=playlists)

# manually adding values to Users table using the UsersandPlaylis.html:
@app.route('/add_user', methods=['POST'])
def add_user():
    add_email = flask.request.form.get('email')
    add_username = flask.request.form.get('username')
    add_password = flask.request.form.get('password')

    new_user = Users(
        email=add_email,
        username=add_username,
        password=generate_password_hash(add_password, method='sha256')
    )
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('UsersAndPlaylist'))

# deleting values from Users table
@app.route('/delete_user', methods=['POST'])
def delete_user():
    user_email = flask.request.form.get('user_email')
    user = Users.query.filter_by(email=user_email).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('UsersAndPlaylist'))

# landing page
@app.route("/")
def main():
    # if session.get('logged_in'):
    # goes straight to playlist page if user already logged in. will finish this when we have log out function
    # return flask.render_template('userPlaylistpage.html')
    # else:
    return flask.render_template('landingpage.html')

# landheader.html
@app.route('/header')
def header():
    return flask.render_template('landheader.html')

#homeheader.html
@app.route('/homeheader')
def homeheader():
    if request.method == 'POST':
        session['logged_in'] = False
    return flask.render_template('homeheader.html')

#landfooter.html
@app.route('/footer')
def footer():
    return flask.render_template('landfooter.html')

# homeheader.html
@app.route('/homeheader')
def homeheader():
    return flask.render_template('homeheader.html')

# uponsigninfooter.html
@app.route('/uponsigninfooter')
def uponsigninfooter():
    return flask.render_template('uponsigninfooter.html')

# signup.html
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        # if this returns a user, then the email already exists in database
        user = Users.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists')
            return flask.render_template('signup.html')

        # if the email address is not in the database
        new_user = Users(
            email=email,
            username=username,
            # hashing the password
            password=generate_password_hash(password, method='sha256')
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Account created!')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

# login.html
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = Users.query.filter_by(email=email).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            # if the user doesn't exist or password is wrong, reload the page
            return redirect(url_for('login'))

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        return flask.render_template('userPlaylistpage.html', username=current_user.username)

    return flask.render_template('login.html')

#userPlaylistpage.html
@app.route('/userpl')
def userpl():
    return flask.render_template('userPlaylistpage.html')

#playlistpage.html
@app.route('/playlist')
def playlist():
    return flask.render_template('playlistpage.html')

# createPlaylistPage.html
@app.route('/createPlaylistPage')
def createPlaylistPage():
    return flask.render_template('createPlaylistPage.html')

#playlistpage.html
@app.route('/playlistpage', methods=['POST', 'GET'])
def playlist_page():
    form_data = flask.request.args
    query = form_data.get("song", "smooth operator")
    results = search_song(query)
    (songResults, artistResults, songIDs) = results
    return flask.render_template(
        'playlistpage.html',
        songResults = songResults,
        artistResults = artistResults,
        songIDs = songIDs
        )

app.secret_key = os.urandom(12)
app.run(debug=True)
