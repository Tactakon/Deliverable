"""
This module serves as the main entry point for our Python program, Verge. 
It contains code that initializes the application and begins the primary execution loop. 
Additionally, this module contains the majority of the application's functionality, 
including logic for data processing, user interaction, and system management.
"""

import os
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import logging
import requests
from search import search_song
import random
import json
import flask
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user, login_user, UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from search import search_song
from databasefunctions import (
    AddSongtoPlaylist, RemoveSongFromPlaylist, AddSharedUserByPlaylistCreator
)


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
    """
    Load the user associated with the given user ID.

    Args:
        user_id (int): The ID of the user to load.

    Returns:
        A User object representing the loaded user.
    """
    return Users.query.get(int(user_id))

# database models


class Users(UserMixin, db.Model):
    """
    Represents a user in the application.

    Attributes:
        id (int): The unique identifier for the user.
        email (str): The user's email address.
        username (str): The user's username.
        password (str): The user's hashed password.
        followers (str): A string representation of the user's followers.
        playlists (list[Playlists]): A list of playlists owned by the user.

    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256))
    username = db.Column(db.String(16))
    password = db.Column(db.String(16))
    followers = db.Column(db.String(1024))
    playlists = db.relationship("Playlists", back_populates="user")

# define the get_id method for Flask-Login
    def get_id(self):
        return self.id


# pylint: disable=too-few-public-methods
class Playlists(db.Model):
    """
    Represents a playlist in the application.

    Attributes:
        id (int): The unique identifier for the playlist.
        name (str): The name of the playlist.
        password (str): The password for the playlist (if any).
        songs (str): A string representation of the songs in the playlist.
        creator (int): The user ID of the playlist's creator.
        listeners_shared_to (str): A string representation of the 
        listeners the playlist is shared with.
        user (User): The User object representing the playlist's owner.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    password = db.Column(db.String(16))
   # playlist_image = db.Column(db.LargeBinary)
    songs = db.Column(db.String(10000))
    creator = db.Column(db.Integer, db.ForeignKey(
        'users.id'))  # user.id stored
    listeners_shared_to = db.Column(db.String(1024))
    user = db.relationship("Users", back_populates="playlists")


with app.app_context():
    db.create_all()

# displaying the Users and Playlist model


# pylint: disable=invalid-name
@app.route('/UsersAndPlaylist')
def UsersAndPlaylist():
    """
    Display all users and playlists in the application.

    Returns:
        A rendered HTML template showing all users and playlists.
    """
    users = Users.query.all()
    playlists = Playlists.query.all()
    return render_template("UsersAndPlaylist.html", users=users, playlists=playlists)

# manually adding values to Users table using the UsersandPlaylist.html:


@app.route('/add_user', methods=['POST'])
def add_user():
    """
    Add a new user to the database.

    Returns:
        A redirect to the UsersAndPlaylist page.
    """
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
    """
    Delete a user from the database.

    Returns:
        A redirect to the UsersAndPlaylist page.
    """
    user_email = flask.request.form.get('user_email')
    user = Users.query.filter_by(email=user_email).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('UsersAndPlaylist'))

# landing page


@app.route("/")
def main():
    """
    Display the landing page of the application.

    Returns:
        A rendered HTML template of the landing page.
    """
    # if session.get('logged_in'):
    # goes straight to playlist page if user already logged in.
    # will finish this when we have log out function
    # return flask.render_template('userPlaylistpage.html')
    # else:
    return flask.render_template('landingpage.html')

# landheader.html


@app.route('/header')
def header():
    """
    Display the header section of the application's landing page.

    Returns:
        A rendered HTML template of the header section of the landing page.
    """
    return flask.render_template('landheader.html')

# homeheader.html


@app.route('/homeheader')
def homeheader():
    """
    Display the header section of the application's playlist page.

    Returns:
        A rendered HTML template of the header section of the playlist page.
    """
    return flask.render_template('homeheader.html')

# landfooter.html


@app.route('/footer')
def footer():
    """
    Display the footer section of the application's landing page.

    Returns:
        A rendered HTML template of the footer section of the landing page.
    """
    return flask.render_template('landfooter.html')

# uponsigninfooter.html


@app.route('/uponsigninfooter')
def uponsigninfooter():
    """
    Display the footer section of the application's playlist page.

    Returns:
        A rendered HTML template of the footer section of the playlist page.
    """
    return flask.render_template('uponsigninfooter.html')

# Json objects declared
# while creating a new user
# followers --> user ids

# signup.html


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    """
    Create a new user account in the database.

    Returns:
        If the request method is GET, a rendered HTML template of the signup page.
        If the request method is POST, a redirect to the login page if the 
        account was created successfully,
        otherwise a rendered HTML template of the signup page with an error message.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        added_to_db = AddUserToDB(email, username, password)
        if added_to_db:
            flash('Account created!')
            return redirect(url_for('login'))
        else:
            flash('Email address already exists')
            return render_template('signup.html')

    return render_template('signup.html')

def AddUserToDB(email, username, password):
    # Check if user already exists
    user = Users.query.filter_by(email=email).first()
    if user:
        return False

    # Add new user to database
    followers_user_ids = []  # empty json object
    new_user = Users(
        email=email,
        username=username,
        password=generate_password_hash(password, method='sha256'),
        followers=json.dumps(followers_user_ids)
    )
    db.session.add(new_user)
    db.session.commit()

    return True

# login.html

@app.route('/login', methods=['POST', 'GET'])
def login():
    """
    Log a user into the application.

    Returns:
        If the request method is GET, a rendered HTML template of the login page.
        If the request method is POST, a redirect to the user's playlist 
        page if the login was successful,
        otherwise a rendered HTML template of the login page with an error message.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))

        user = Users.query.filter_by(email=email).first()

        # check if the user actually exists
        # take the user-supplied password, hash it,
        # and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            # if the user doesn't exist or password is wrong, reload the page
            return redirect(url_for('login'))

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)

        playlists = Playlists.query.filter_by(
            creator=current_user.id).all()[:3]
        return flask.render_template('userPlaylistpage.html', username=current_user.username, current_user_playlists=playlists)

    return flask.render_template('login.html')

# Json objects declared
# while creating a new playlist
# listeners shared to -- > user ids
# songs --> song ids

# createPlaylistPage.html

@app.route('/createPlaylistPage', methods=['GET', 'POST'])
@login_required
def createPlaylistPage():
    """
    Renders the create playlist page and handles the creation of new playlists.

    Returns:
        If the request method is GET, a rendered HTML template of the create playlist page.
        If the request method is POST and the playlist was created successfully, 
        a redirect to the playlist page.
        Otherwise, a rendered HTML template of the create playlist page with an error message.
    """
    if request.method == 'POST':
        # Retrieve form data
        playlist_name = request.form.get('playlist-name')
        playlist_passcode = request.form.get('playlist-passcode')
        playlist_image = request.files.get('playlist-image')

        # intialize empty json objects of the songs and listeners_shared_to
        songs = []
        listeners_shared_to = []


        # Create new playlist object
        new_playlist = Playlists(
            name=playlist_name,
            password=playlist_passcode,
            creator=current_user.id,
            songs=json.dumps(songs),  # now a json string
            listeners_shared_to=json.dumps(
                listeners_shared_to)  # now a json string
        )

        # If a playlist image was uploaded, save it to the new playlist

        #If a playlist image was uploaded, save it to the new playlist
        if playlist_image:
            # pylint: disable=attribute-defined-outside-init
            new_playlist.playlist_image = playlist_image.read()

        # Add new playlist to the database
        db.session.add(new_playlist)
        db.session.commit()

        flash('Playlist created!')
        return redirect(url_for('playlistpage',
        username=current_user.username,
        playlist_name=playlist_name,
        songs=songs)) ## want to send a dict so that it could loop

    return flask.render_template('createPlaylistPage.html', username=current_user.username)


# playlistpage


@login_required
@app.route('/playlistpage', methods=['POST', 'GET'])
def playlistpage():
    """
    Renders the playlist page and handles the addition and removal of songs from the playlist.

    Returns:
        If the request method is GET, a rendered HTML template of the playlist page.
        If the request method is POST and a song was added or removed from the playlist,
        a redirect back to the playlist page.
        Otherwise, a rendered HTML template of the playlist page with an error message.
    """
    username = request.args.get('username')
    playlist_name = request.args.get('playlist_name')

    playlist = Playlists.query.filter_by(
        name=playlist_name, creator=current_user.id).first()
    if playlist.songs:
        songs = json.loads(playlist.songs)
    else:
        songs = []

    # API
    form_data = request.args
    query = form_data.get("song", "smooth operator")
    results = search_song(query)
    (songResults, artistResults, songIDs) = results

    return render_template(
        'playlistpage.html',
        username=username,
        playlist_name=playlist_name,
        songs=songs,  # dict
        songResults=songResults,
        artistResults=artistResults,
        songIDs=songIDs
    )


@app.route("/AddSharedUserByPlaylistOwner", methods=["POST"])
def AddSharedUserByPlaylistOwner():
    """
    Renders the playlist page and handles the addition and removal of songs from the playlist.

    Returns:
        If the request method is GET, a rendered HTML template of the playlist page.
        If the request method is POST and a song was added or removed from the playlist,
        a redirect back to the playlist page.
        Otherwise, a rendered HTML template of the playlist page with an error message.
    """
    username = request.form.get('username')
    playlist_name = request.form.get('playlist_name')
    shareduser_username = request.form.get('shareduser_username')

    shareduser = Users.query.filter_by(username=shareduser_username).first()

    playlist = Playlists.query.filter_by(
        name=playlist_name, creator=current_user.id).first()
    print(playlist)
    print(playlist.listeners_shared_to)
    print(shareduser.id)

    playlist.listeners_shared_to = AddSharedUserByPlaylistCreator(
        playlist.listeners_shared_to, shareduser.id)
    print(playlist.listeners_shared_to)

    db.session.commit()

    return redirect(url_for('playlistpage', username=current_user.username, playlist_name=playlist_name, songs=json.loads(playlist.songs)))


@app.route("/AddSong", methods=["POST"])
@login_required
def AddSong():
    username = request.form.get('username')
    playlist_name = request.form.get('playlist_name')

    playlist = Playlists.query.filter_by(
        name=playlist_name, creator=current_user.id).first()

    songID = request.form.get('songID')
    songResult = request.form.get('songResult')
    artistResult = request.form.get('artistResult')

    # calling AddSongToPlaylist function from databasefunctions.py
    playlist.songs = AddSongtoPlaylist(
        playlist.songs, songID, songResult, artistResult)

    db.session.commit()

    return redirect(url_for('playlistpage', username=current_user.username, playlist_name=playlist_name, songs=json.loads(playlist.songs)))


@app.route("/DeleteSong", methods=["POST"])
@login_required
def DeleteSong():
    username = request.form.get('username')
    playlist_name = request.form.get('playlist_name')

    playlist = Playlists.query.filter_by(
        name=playlist_name, creator=current_user.id).first()

    songID = request.form.get('songID')
    songResult = request.form.get('songResult')
    artistResult = request.form.get('artistResult')

    # calling RemoveSongFromPlaylist function from databasefunctions.py
    playlist.songs = RemoveSongFromPlaylist(
        playlist.songs, songID, songResult, artistResult)

    db.session.commit()

    return redirect(url_for('playlistpage', username=current_user.username, playlist_name=playlist_name, songs=json.loads(playlist.songs)))

# userPlaylistpage.html


@app.route('/userPlaylistpage')
@login_required
def userPlaylistpage():
    playlists = Playlists.query.filter_by(creator=current_user.id).all()[:3]
    return flask.render_template('userPlaylistpage.html', username=current_user.username, current_user_playlists=playlists)

# PlaylistMore.html


@app.route('/PlaylistMore')
def PlaylistMore():
    return flask.render_template('PlaylistMore.html')


app.secret_key = os.urandom(12)
app.run(debug=True)