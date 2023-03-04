import flask
import os
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import logging
import requests
from search import search_song
from flask_login import login_required, current_user, login_user, UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import json

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
    followers = db.Column(db.String(1024))
    playlists = db.relationship("Playlists", back_populates="user")

# define the get_id method for Flask-Login
    def get_id(self):
        return self.id

class Playlists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    password = db.Column(db.String(16))
   # playlist_image = db.Column(db.LargeBinary)
    songs = db.Column(db.String(10000))
    creator = db.Column(db.Integer, db.ForeignKey('users.id')) #user.id stored
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

# manually adding values to Users table using the UsersandPlaylist.html:
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
    return flask.render_template('homeheader.html')

#landfooter.html
@app.route('/footer')
def footer():
    return flask.render_template('landfooter.html')

# uponsigninfooter.html
@app.route('/uponsigninfooter')
def uponsigninfooter():
    return flask.render_template('uponsigninfooter.html')

# Json objects declared
# while creating a new user
# followers --> user ids

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
        
        followers_user_ids = [] #empty json object

        # if the email address is not in the database
        new_user = Users(
            email=email,
            username=username,
            # hashing the password
            password=generate_password_hash(password, method='sha256'),
            followers = json.dumps(followers_user_ids)
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
        

        playlists = Playlists.query.filter_by(creator=current_user.id).all()[:3]
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
    if request.method == 'POST':
        # Retrieve form data
        playlist_name = request.form.get('playlist-name')
        playlist_passcode = request.form.get('playlist-passcode')
        playlist_image = request.files.get('playlist-image')

        #intialize empty json objects of the songs and listeners_shared_to
        songs = []
        listeners_shared_to = []
        
        # Create new playlist object
        new_playlist = Playlists(
            name=playlist_name, 
            password=playlist_passcode, 
            creator=current_user.id,
            songs=json.dumps(songs), # now a json string
            listeners_shared_to=json.dumps(listeners_shared_to)  # now a json string
        )
        
        #If a playlist image was uploaded, save it to the new playlist  
        if playlist_image:
            new_playlist.playlist_image = playlist_image.read()

        # Add new playlist to the database
        db.session.add(new_playlist)
        db.session.commit()

        flash('Playlist created!')
        return redirect(url_for('playlistpage', username=current_user.username, playlist_name=playlist_name, songs=songs)) ## want to send a dict so that it could loop
    
    return flask.render_template('createPlaylistPage.html', username=current_user.username)

# playlistpage
@login_required
@app.route('/playlistpage', methods=['POST', 'GET'])
def playlistpage():
    username = request.args.get('username')
    playlist_name = request.args.get('playlist_name')
    print(request.args.keys())
 
    playlist = Playlists.query.filter_by(
        name=playlist_name, creator=current_user.id).first()
    if playlist.songs:
        songs = json.loads(playlist.songs)
    else:
        songs = []
    
    print("PlaylistPage" , songs)

    #API
    form_data = request.args
    query = form_data.get("song", "smooth operator")
    results = search_song(query)
    (songResults, artistResults, songIDs) = results

    return render_template(
        'playlistpage.html',
        username=username,
        playlist_name=playlist_name,
        songs=songs, #dict
        songResults=songResults,
        artistResults=artistResults,
        songIDs=songIDs
    )


@app.route("/AddSong", methods=["POST"])
@login_required
def AddSong():
    username = request.form.get('username')
    playlist_name = request.form.get('playlist_name')
    print("addsong keys", request.form)
    print(playlist_name)
   
    playlist = Playlists.query.filter_by(
        name=playlist_name, creator=current_user.id).first()
    print("Current Playlist", playlist)
    if playlist.songs != '[]':
        songs = json.loads(playlist.songs)
    else:
        songs = []

    print("Add Songs:" , songs)

    songID = request.form.get('songID')
    print(songID)
    songResult = request.form.get('songResult')
    print(songResult)
    artistResult = request.form.get('artistResult')
    print(artistResult)

    song = {
        "songID": songID,
        "songResult": songResult,
        "artistResult": artistResult
    }

    songs.append(song)
    print("Addes SONG: " , songs)
    playlist = Playlists.query.filter_by(name=playlist_name, creator=current_user.id).first()
    print("Playlist in which the song is added: ", playlist)
    if playlist is not None:
        playlist.songs = json.dumps(songs)

    db.session.commit()

    return redirect(url_for('playlistpage', username=current_user.username, playlist_name=playlist_name, songs=songs))

@app.route("/DeleteSong", methods=["POST"])
@login_required
def DeleteSong():
    username = request.form.get('username')
    playlist_name = request.form.get('playlist_name')
    print("addsong keys", request.form)
    print(playlist_name)

    playlist = Playlists.query.filter_by(
        name=playlist_name, creator=current_user.id).first()
    print("Current Playlist", playlist)
    if playlist.songs != '[]':
        songs = json.loads(playlist.songs)
    else:
        songs = []

    print("remove Songs:", songs)

    songID = request.form.get('songID')
    print(songID)
    songResult = request.form.get('songResult')
    print(songResult)
    artistResult = request.form.get('artistResult')
    print(artistResult)

    song = {
        "songID": songID,
        "songResult": songResult,
        "artistResult": artistResult
    }

    songs.remove(song)
    print("removed SONG: ", songs)
    playlist = Playlists.query.filter_by(
        name=playlist_name, creator=current_user.id).first()
    print("Playlist in which the song is removes: ", playlist)
    if playlist is not None:
        playlist.songs = json.dumps(songs)

    db.session.commit()

    return redirect(url_for('playlistpage', username=current_user.username, playlist_name=playlist_name, songs=songs))

    
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