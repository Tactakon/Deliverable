"""
This module serves as the main entry point for our Python program, Verge. 
It contains code that initializes the application and begins the primary execution loop. 
Additionally, this module contains the majority of the application's functionality, 
including logic for data processing, user interaction, and system management.
"""

import os
import random
import json
import flask
import requests
from flask import flash, redirect, render_template, request, url_for, make_response
from flask_login import login_required, current_user, login_user, UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from search import search_song
from databasefunctions import (
    AddSongtoPlaylist, RemoveSongFromPlaylist, AddSharedPlaylistID, AddSharedUserByPlaylistCreator
)


app = flask.Flask(__name__)

@app.errorhandler(Exception)
def handle_exception(e):
    # Log the exception
    app.logger.error(f"Unhandled exception: {str(e)}")
    
    # Render a custom error page
    return render_template('error.html', error=str(e))

basedir = os.path.abspath(os.path.dirname(__file__))

# each user of the app need their secret key #in .env as SECRET_KEY
app.config['SECRET_KEY'] = os.urandom(12)

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

# getting the base url
def get_base_url():
    """
    Returns the base URL of the current request, taking into account any reverse proxy servers.
    :return: A string representing the base URL of the current request.
    """
    scheme = request.headers.get('X-Forwarded-Proto', 'http')
    host = request.headers.get('X-Forwarded-Host', request.host)
    return f'{scheme}://{host}'

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
        shared_playlists (str): A string representation of the 
        playlists that are shared with the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256))
    username = db.Column(db.String(16))
    password = db.Column(db.String(16))
    followers = db.Column(db.String(1024))
    shared_playlists = db.Column(db.String(1024))
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
        description (str): The description for the playlist (if any).
        playlist_image (db.LargeBinary): The image data for the playlist.
        songs (str): A string representation of the songs in the playlist.
        creator (int): The user ID of the playlist's creator.
        listeners_shared_to (str): A string representation of the 
        users with whom the playlist is shared with.
        user (User): The User object representing the playlist's owner.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    password = db.Column(db.String(16))
    description = db.Column(db.String(10000))
    playlist_image = db.Column(db.LargeBinary)
    songs = db.Column(db.String(10000))
    playlist_genre = db.Column(db.String(100))
    creator = db.Column(db.Integer, db.ForeignKey(
        'users.id'))  # user.id stored
    listeners_shared_to = db.Column(db.String(1024))
    user = db.relationship("Users", back_populates="playlists")

class Notification(db.Model):
    """
    Represents a notification in the application.
    Attributes:
        id (int): The unique identifier for the notification.
        message (str): The message to be displayed in the notification.
        action (str): The playlist on which the action is taken
        timestamp (datetime): The timestamp of when the notification was created.
        users (list[Users]): A list of users associated with the notification.
    """
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(10000))
    action = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    users = db.relationship('Users', secondary='notification_users')

class NotificationUsers(db.Model):
    """
    Represents the many-to-many relationship between notifications and users.
    Attributes:
        notification_id (int): The ID of the notification associated with the relationship.
        user_id (int): The ID of the user associated with the relationship.
        read (bool): Whether the notification has been read by the associated user.
    """
    notification_id = db.Column(db.Integer, db.ForeignKey(
        'notification.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)
    read = db.Column(db.Boolean, default=False)

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
    shared_playlists = []
    new_user = Users(
        email=add_email,
        username=add_username,
        password=generate_password_hash(add_password, method='sha256'),
        playlists_shared_with=json.dumps(shared_playlists)
    )
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('UsersAndPlaylist'))

# error tester
@app.route('/error')
def error():
    raise ValueError("An error occurred")

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

#################
@app.route('/NotificationDatabaseViewer')
def NotificationDatabaseViewer():
    """
    Renders the Notification Database Viewer page, which displays a table of notifications
    and their associated users, as well as a table of notification-user relationships.
    """
    # Replace this with your database query logic
    notifications = Notification.query.all()
    notification_users = NotificationUsers.query.all()

    return render_template('NotificationDatabaseViewer.html',
                           notifications=notifications,
                           notification_users=notification_users)

@app.route('/notifications')
@login_required
def notifications():

    # Get all notifications associated with the user
    user_notifications = NotificationUsers.query.filter_by(
        user_id=current_user.id).all()
    

    all_notificatons = []

    for user_notification in user_notifications:
        user_notification.read = True
        print( user_notification.read)
        print(user_notification.notification_id)
        #getting the notification ID from the notificationUsers table
        id_notification = user_notification.notification_id
        #getting the notification from the notification table
        notification = Notification.query.filter_by(
            id=id_notification).first()
        all_notificatons.append(notification)

    db.session.commit()

    return render_template("notifications.html", notifications=all_notificatons)

#Getting the playlist image
@app.route('/playlist_image/<int:playlist_id>')
def playlist_image(playlist_id):
    """
    Returns the playlist image for the given playlist ID.
    Args:
        playlist_id (int): The ID of the playlist.
    Returns:
        flask.Response: The playlist image as a Flask response object with the correct MIME type.
    """
    playlist = Playlists.query.get_or_404(playlist_id)
    response = make_response(playlist.playlist_image)
    response.headers.set('Content-Type', 'image/jpeg')
    return response


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
    unread_count = NotificationUsers.query.filter_by(
        user_id=current_user.id, read=False).count()
    return flask.render_template('homeheader.html', unread_count=unread_count)

#searching playlist
@app.route('/playlistsearch')
@login_required
def playlistsearch():
    """
    Searches for a playlist by name and filters songs based on genre and query parameters.

    Parameters:
    None

    Returns:
    A redirect to the sharedplaylistpage route with the following parameters:
    - username: the username of the user who created the playlist
    - playlist_name: the name of the playlist
    - playlist_creator: the username of the user who created the playlist
    - songs: a list of songs in the playlist
    - genre: the genre of the playlist
    - songResults: a list of song results from the API search
    - artistResults: a list of artist results from the API search
    - songIDs: a list of song IDs from the API search
    - imageURLs: a list of image URLs from the API search
    """
    username = request.args.get('username')
    search_query = request.args.get('search-query')
    selected_genre = request.args.get('genre')
    playlist = Playlists.query.filter(
        Playlists.name.like(f'%{search_query}%')).first()
    
    playlist_creator = Users.query.filter_by(id=playlist.creator).first()
    playlist_creator = playlist_creator.username

    if playlist is None:
        # Playlist not found, handle error
        return "Playlist not found"

    if playlist.songs:
        songs = json.loads(playlist.songs)
    else:
        songs = []

    # API
    form_data = request.args
    query = form_data.get("song", "smooth operator")
    q = f'genre:{selected_genre} track:{query}'
    results = search_song(q)
    (songResults, artistResults, songIDs, imageURLs) = results

    return redirect(url_for('sharedplaylistpage',
                            username=username,
                            playlist_name=playlist.name,
                            playlist_creator=playlist_creator,
                            songs=songs,
                            genre=playlist.playlist_genre,
                            songResults=songResults,
                            artistResults=artistResults,
                            songIDs=songIDs,
                            imageURLs=imageURLs
                            ))

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
        # pylint: disable = no-else-return
        if added_to_db:
            flash('Account created!')

            # Retrieve the newly created user object
            user = Users.query.filter_by(email=email).first()

            # Log the user in
            login_user(user)

            # Redirect to the userPlaylistpage
            return redirect(url_for('userPlaylistpage'))
        else:
            flash('Email address already exists')
            return render_template('signup.html')

    return render_template('signup.html')


def AddUserToDB(email, username, password):
    """
    Adds a new user to the database.
    Args:
        email (str): The email address of the new user.
        username (str): The username of the new user.
        password (str): The password of the new user.
    Returns:
        bool: True if the user was added to the database successfully, 
        False if a user with the same email already exists in the database.
    """
    # Check if user already exists
    user = Users.query.filter_by(email=email).first()
    if user:
        return False

    # Add new user to database
    followers_user_ids = []  # empty json object
    shared_playlists = []  # empty json object
    new_user = Users(
        email=email,
        username=username,
        password=generate_password_hash(password, method='sha256'),
        followers=json.dumps(followers_user_ids),
        shared_playlists=json.dumps(shared_playlists)
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

        # Redirect the user to their playlist page
        return redirect(url_for('userPlaylistpage'))

    return render_template('login.html')

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
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Retrieve form data
        playlist_name = request.form.get('playlist-name')
        playlist_description = request.form.get('playlist-description')
        playlist_passcode = request.form.get('playlist-passcode')
        playlist_image = request.files.get('playlist-image')
        selected_genre = request.form['playlist-genre']

        # intialize empty json objects of the songs and listeners_shared_to
        songs = []
        listeners_shared_to = []

        # Create new playlist object
        new_playlist = Playlists(
            name=playlist_name,
            password=playlist_passcode,
            description=playlist_description,
            creator=current_user.id,
            playlist_genre = selected_genre,
            songs=json.dumps(songs),  # now a json string
            listeners_shared_to=json.dumps(
                listeners_shared_to)  # now a json string
        )

        static_folder = os.path.abspath('static')

        # get a list of all the images in the imgsmall folder
        images_folder = os.path.join(static_folder, 'images', 'imgsmall')
        images = os.listdir(images_folder)
        images = [img for img in images if img.endswith(
            ('.jpg', '.jpeg', '.png'))]

        # select a random image from the list
        random_image = random.choice(images)

        # Generate the image URL
        base_url = get_base_url()
        image_url = f'{base_url}{url_for("static", filename=f"images/imgsmall/{random_image}")}'

        # If a playlist image was uploaded, save it to the new playlist
        if playlist_image:
            # pylint: disable=attribute-defined-outside-init
            new_playlist.playlist_image = playlist_image.read()
        # If a playlist image was not uploaded, randomly select and save it
        else:
            # read the image file as bytes using requests module
            image_bytes = requests.get(image_url).content

            # save the image bytes to the new playlist
            new_playlist.playlist_image = image_bytes

        # Add new playlist to the database
        db.session.add(new_playlist)
        db.session.commit()

        flash('Playlist created!')
        return redirect(url_for('playlistpage',
                                username=current_user.username,
                                playlist_name=playlist_name,
                                genre=selected_genre,
                                songs=songs))  # want to send a dict so that it could loop

    # if the request method is GET
    return flask.render_template('createPlaylistPage.html', username=current_user.username)

# playlistpage
@login_required
@app.route('/playlistpage', methods=['POST', 'GET'])
@login_required
def playlistpage():
    """
    Renders the playlist page and handles the addition and removal of songs from the playlist.
    Returns:
        If the request method is GET, a rendered HTML template of the playlist page.
        If the request method is POST and a song was added or removed from the playlist,
        a redirect back to the playlist page.
        Otherwise, a rendered HTML template of the playlist page with an error message.
    """
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    username = request.args.get('username')
    playlist_name = request.args.get('playlist_name')
    selected_genre = request.args.get('genre')

    playlist = Playlists.query.filter_by(
        name=playlist_name).first()
    description = playlist.description

    #Error handling if songs is empty
    if playlist != None and playlist.songs: 
        songs = json.loads(playlist.songs)
    else:
        songs = []

    # API
    form_data = request.args
    query = form_data.get("song", "smooth operator")
    q = f'genre:{selected_genre} track:{query}'
    results = search_song(q)
    (songResults, artistResults, songIDs, imageURLs) = results


    return render_template(
        'playlistpage.html',
        username=username,
        playlist_name=playlist_name,
        description=description,
        songs=songs,  # dict
        genre=playlist.playlist_genre,
        songResults=songResults,
        artistResults=artistResults,
        songIDs=songIDs,
        imageURLs=imageURLs
    )

#Adding a shared user
@app.route("/AddSharedUserByPlaylistOwner", methods=["POST"])
@login_required
def AddSharedUserByPlaylistOwner():
    """
    Add a shared user to a playlist owned by the current user.
    Input:
    - username: the username of the current user
    - playlist_name: the name of the playlist to add the shared user to
    - shareduser_username: the username of the user to share the playlist with
    Output:
    - redirect to the playlist page with the updated shared listeners list
    """
    # pylint: disable=unused-variable
    username = request.form.get('username')
    playlist_name = request.form.get('playlist_name')
    shareduser_username = request.form.get('shareduser_username')
    selected_genre = request.args.get('genre')

    shareduser = Users.query.filter_by(username=shareduser_username).first()

    playlist = Playlists.query.filter_by(
        name=playlist_name, creator=current_user.id).first()
    print(playlist)
    print(shareduser.shared_playlists)
    print(shareduser.id)

    #adding to shared playlists
    shareduser.shared_playlists = AddSharedPlaylistID(
        shareduser.shared_playlists, playlist.id)
    print(shareduser.shared_playlists)

    #adding to listeners shared to
    playlist.listeners_shared_to = AddSharedUserByPlaylistCreator(
        playlist.listeners_shared_to, shareduser.id)
    print(playlist.listeners_shared_to)

    db.session.commit()

    return redirect(url_for('playlistpage',
                            username=current_user.username,
                            playlist_name=playlist_name,
                            genre=selected_genre,
                            songs=json.loads(playlist.songs)))

#Adding song to the playlist
@app.route("/AddSong", methods=["POST"])
@login_required
def AddSong():
    """
    Adds a song to a playlist.
    Returns:
    A redirect to the playlist page with the newly added song displayed.
    """
    # pylint: disable=unused-variable
    username = request.form.get('username')
    playlist_name = request.form.get('playlist_name')
    selected_genre = request.args.get('genre')

    playlist = Playlists.query.filter_by(
        name=playlist_name).first()
    
    if playlist is None:
     # You can return an error message or redirect to another page if the playlist is not found
        return "Playlist not found", 404

    songID = request.form.get('songID')
    songResult = request.form.get('songResult')
    artistResult = request.form.get('artistResult')
    imageURL = request.form.get('imageURL')

    # calling AddSongToPlaylist function from databasefunctions.py
    playlist.songs = AddSongtoPlaylist(
        playlist.songs, songID, songResult, artistResult, imageURL)

    db.session.commit()

    # Create a notification when a song is added to a playlist
    notification = Notification(
        message=f"{songResult} has been added to {playlist.name} by {current_user.username}.",
        action=playlist.name,
        timestamp=datetime.utcnow()
    )

    # Convert the string to a list of dictionaries
    listeners_shared_to = json.loads(playlist.listeners_shared_to)

    # Add users who should receive the notification
    creator = Users.query.get(playlist.creator)
    notification.users.append(creator)  # CREATOR

    # SHARED
    for listener in listeners_shared_to:
        shared_user_id = listener.get("sharedUserID")
        shared_user = Users.query.get(shared_user_id)
        notification.users.append(shared_user)

    # Add the notification to the session
    db.session.add(notification)

    # Commit the session to save the notification to the database
    db.session.commit()

    return redirect(url_for('playlistpage',
                            username=current_user.username,
                            playlist_name=playlist_name,
                            songs=json.loads(playlist.songs)))

# sharedplaylistpage
@app.route('/sharedplaylistpage', methods=['POST', 'GET'])
@login_required
def sharedplaylistpage():
    """
    Renders the page for a shared playlist.
    """
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    username = request.args.get('username')
    playlist_name = request.args.get('playlist_name', '')
    selected_genre = request.args.get('genre')

    playlist = Playlists.query.filter_by(
        name=playlist_name).first()
    description = playlist.description

    playlist = Playlists.query.filter_by(
        name=playlist_name).first()
    if playlist and playlist.songs:
        songs = json.loads(playlist.songs)
    else:
        songs = []

    playlist_creator = Users.query.filter_by(id=playlist.creator).first()
    playlist_creator = playlist_creator.username

    # API
    form_data = request.args
    query = form_data.get("song", "smooth operator")
    q = f'genre:{selected_genre} track:{query}'
    results = search_song(q)
    (songResults, artistResults, songIDs, imageURLs) = results

    return render_template(
        'sharedplaylistpage.html',
        username=username,
        playlist_name=playlist_name,
        playlist_creator=playlist_creator,
        description=description,
        songs=songs,  # dict
        genre=playlist.playlist_genre,
        songResults=songResults,
        artistResults=artistResults,
        songIDs=songIDs,
        imageURLs=imageURLs
    )

#Shared User adding Song
@app.route("/AddSongBySharedUser", methods=["POST"])
@login_required
def AddSongBySharedUser():
    """
    Adds a song to a shared playlist if the password provided by the user is correct.
    """
    # pylint: disable=unused-variable
    username = request.form.get('username')
    playlist_name = request.form.get('playlist_name')
    password = request.form.get('password')
    selected_genre = request.args.get('genre')
    playlist = Playlists.query.filter_by(name=playlist_name).first()

    # Check if the password entered by the user matches the password in the database
    if playlist.password == password:
        print('Song Added')
    else:
        print('Password is incorrect.')
        return redirect(url_for('sharedplaylistpage',  playlist_name=playlist_name, username=username))

    playlist = Playlists.query.filter_by(
        name=playlist_name).first()

    songID = request.form.get('songID')
    songResult = request.form.get('songResult')
    artistResult = request.form.get('artistResult')
    imageURL = request.form.get('imageURL')

    # calling AddSongToPlaylist function from databasefunctions.py
    playlist.songs = AddSongtoPlaylist(
        playlist.songs, songID, songResult, artistResult, imageURL)

    db.session.commit()
 
  # Create a notification when a song is added to a playlist
    notification = Notification(
        message=f"{songResult} has been added to {playlist.name} by {current_user.username}.",
        action=playlist.name,
        timestamp=datetime.utcnow()
    )
    print(notification)

    # Convert the string to a list of dictionaries
    listeners_shared_to = json.loads(playlist.listeners_shared_to)

    # Add users who should receive the notification
    creator = Users.query.get(playlist.creator)
    notification.users.append(creator)  # CREATOR
    print("Creator ", notification.users)

    # SHARED
    for listener in listeners_shared_to:
        shared_user_id = listener.get("sharedUserID")
        shared_user = Users.query.get(shared_user_id)
        notification.users.append(shared_user)

    if current_user not in notification.users:
        notification.users.append(current_user)

    # Add the notification to the session
    db.session.add(notification)

    # Commit the session to save the notification to the database
    db.session.commit()

    # no longer requires password after first song added
    return redirect(url_for('playlistpage',
                            username=current_user.username,
                            playlist_name=playlist_name,
                            genre=playlist.playlist_genre,
                            songs=json.loads(playlist.songs)))

#Deleting song
@app.route("/DeleteSong", methods=["POST"])
@login_required
def DeleteSong():
    """
    Deletes a song from a playlist.
    Returns:
    A redirect to the playlist page with the newly deleted song displayed.
    """
    # pylint: disable=unused-variable
    username = request.form.get('username')
    playlist_name = request.form.get('playlist_name')
    selected_genre = request.args.get('genre')

    playlist = Playlists.query.filter_by(
        name=playlist_name).first()

    songID = request.form.get('songID')
    songResult = request.form.get('songResult')
    artistResult = request.form.get('artistResult')
    imageURL = request.form.get('imageURL')

    # calling RemoveSongFromPlaylist function from databasefunctions.py
    playlist.songs = RemoveSongFromPlaylist(
        playlist.songs, songID, songResult, artistResult, imageURL)
        
  # Create a notification when a song is added to a playlist
    notification = Notification(
        message=f"{songResult} has been deleted from {playlist.name} by {current_user.username}.",
        action=playlist.name,
        timestamp=datetime.utcnow()
    )
    
    # Convert the string to a list of dictionaries
    listeners_shared_to = json.loads(playlist.listeners_shared_to)

    # Add users who should receive the notification
    creator = Users.query.get(playlist.creator)
    notification.users.append(creator)  # CREATOR

    # SHARED
    for listener in listeners_shared_to:
        shared_user_id = listener.get("sharedUserID")
        shared_user = Users.query.get(shared_user_id)
        notification.users.append(shared_user)

    if current_user not in notification.users:
        notification.users.append(current_user)

    # Add the notification to the session
    db.session.add(notification)

    # Commit the session to save the notification to the database
    db.session.commit()
    
    return redirect(url_for('playlistpage',
                            username=current_user.username,
                            playlist_name=playlist_name,
                            genre=playlist.playlist_genre,
                            songs=json.loads(playlist.songs)))

# userPlaylistpage.html
@app.route('/userPlaylistpage')
@login_required
def userPlaylistpage():
    """
    Renders the user's playlist page with their playlists and
    shared playlists displayed.
    Returns:
    A rendered HTML template of the user's playlist page with 
    the user's playlists, shared playlists, and a random image.
    """
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    playlists = Playlists.query.filter_by(creator=current_user.id).all()
    playlists.reverse()

    this_user = Users.query.filter_by(id=current_user.id).first()
    shared_playlists = json.loads(this_user.shared_playlists)
    shared_playlists_with_user = []
    for shared_playlist in shared_playlists:
        shared_playlist_with_user = Playlists.query.filter_by(
            id=shared_playlist['playlistID']).first()
        shared_playlists_with_user.append(shared_playlist_with_user)

    images_dir = os.path.join(app.static_folder, 'images', 'imgsmall')
    random_image = random.choice(os.listdir(images_dir))
    return render_template('userPlaylistpage.html',
                           username=current_user.username,
                           playlists=playlists,
                           shared_playlists=shared_playlists_with_user,
                           random_image=random_image)


# PlaylistMore.html
@app.route('/PlaylistMore')
@login_required
def PlaylistMore():
    """
    Renders the "PlaylistMore.html" template, which displays all of the playlists
    created by the currently logged-in user.
    Returns:
        A rendered HTML template displaying the user's playlists.
    """
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    playlists = get_playlists_by_user_id(current_user.id)
    playlists.reverse()
    # Error handling
    images_dir = os.path.join(app.static_folder, 'images', 'imglarge')
    random_image = random.choice(os.listdir(images_dir))
    return render_template('PlaylistMore.html', playlists=playlists, random_image=random_image)

# SharedPlaylistMore.html
@app.route('/SharedPlaylistMore')
@login_required
def SharedPlaylistMore():
    """
    Renders the 'SharedPlaylistMore.html' template with a list of playlists that have
    been shared with the current logged-in user.
    Returns:
        str: A rendered HTML template with the shared playlists and random image.
    """
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    shared_playlists = get_shared_playlists_by_user_id(current_user.id)
    shared_playlists.reverse()
    # Error handling
    images_dir = os.path.join(app.static_folder, 'images', 'imglarge')
    random_image = random.choice(os.listdir(images_dir))
    return render_template('SharedPlaylistMore.html', shared_playlists=shared_playlists, random_image=random_image)

def get_playlists_by_user_id(user_id):
    """
    Queries the database for all playlists created by the user with the given ID.
    Args:
        user_id: The ID of the user.
    Returns:
        A list of playlist objects created by the user.
    """
    playlists = Playlists.query.filter_by(creator=user_id).all()
    return playlists

# AboutUs.html
@app.route('/AboutUs.html')
def about_us():
    return render_template('AboutUs.html')

# AboutUs2.html
@app.route('/AboutUs2.html')
def about_us2():
    return render_template('AboutUs2.html')

# Support.html
@app.route('/Support.html')
def support():
    return render_template('Support.html')

# Support2.html
@app.route('/Support2.html')
def support2():
    return render_template('Support2.html')

# TermsofUse.html
@app.route('/TermsofUse.html')
def terms_of_use():
    return render_template('TermsofUse.html')

# TermsofUse2.html
@app.route('/TermsofUse2.html')
def terms_of_use2():
    return render_template('TermsofUse2.html')

# PrivacyPolicy.html
@app.route('/PrivacyPolicy.html')
def privacy_policy():
    return render_template('PrivacyPolicy.html')

# PrivacyPolicy2.html
@app.route('/PrivacyPolicy2.html')
def privacy_policy2():
    return render_template('PrivacyPolicy2.html')

def get_shared_playlists_by_user_id(user_id):
    """
    Retrieves the shared playlists of a user with the given ID.

    Args:
        user_id (int): The ID of the user whose shared playlists to retrieve.

    Returns:
        list: A list of playlists that have been shared with the user, represented
        as Playlists objects.

    Raises:
        AttributeError: If the user with the given ID does not exist in the database,
        or if their shared_playlists field is not a valid JSON string.
    """
    this_user = Users.query.filter_by(id=user_id).first()
    shared_playlists = json.loads(this_user.shared_playlists)
    shared_playlists_with_user = []
    for shared_playlist in shared_playlists:
        shared_playlist_with_user = Playlists.query.filter_by(
            id=shared_playlist['playlistID']).first()
        shared_playlists_with_user.append(shared_playlist_with_user)
    return shared_playlists_with_user

if __name__ == "__main__":
    app.run(debug=True)