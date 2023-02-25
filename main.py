import flask
import os
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import logging
import requests
from search import search_song

from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

#database boilerplate code
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

#database models
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256))
    username = db.Column(db.String(16))
    password = db.Column(db.String(16))
    created_playlists = db.Column(db.String(1024))
    playlists_shared_with = db.Column(db.String(1024))
    followers = db.Column(db.String(1024))
    playlists = db.relationship("Playlists", back_populates="user")

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

#displaying the Users and Playlist model
@app.route('/UsersAndPlaylist')
def UsersAndPlaylist():
    users = Users.query.all()
    playlists = Playlists.query.all()
    return render_template("UsersAndPlaylist.html", users=users, playlists=playlists)

#adding values to Users table:
@app.route('/add_user', methods=['POST'])
def add_user():
    add_email = flask.request.form.get('email')
    add_username = flask.request.form.get('username')
    add_password = flask.request.form.get('password')

    new_user = Users(
        email = add_email,
        username = add_username,
        password = add_password
    )

    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('UsersAndPlaylist'))

#deleting values from Users table
@app.route('/delete_user', methods=['POST'])
def delete_user():
    user_email = flask.request.form.get('user_email')
    user = Users.query.filter_by(email=user_email).first()
    db.session.delete(user)
    db.session.commit()   
    return redirect(url_for('UsersAndPlaylist'))

#landing page
@app.route("/")
def main():
    #if session.get('logged_in'):
        #goes straight to playlist page if user already logged in. will finish this when we have log out function
       # return flask.render_template('userPlaylistpage.html')
    #else:
    return flask.render_template('landingpage.html')

#landheader.html
@app.route('/header')
def header():
    return flask.render_template('landheader.html')

#landfooter.html
@app.route('/footer')
def footer():
    return flask.render_template('landfooter.html')

#signup.html
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    return flask.render_template('signup.html')

#login.html
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if flask.request.form['psw'] == 'password' and flask.request.form['email'] == 'admin':
            session['logged_in'] = True
            return redirect('/userpl')
        else:
            flash('wrong password!')
    return flask.render_template('login.html') 

#userPlaylistpage.html
@app.route('/userpl')
def userpl():
    return flask.render_template('userPlaylistpage.html')

#playlistpage.html
@app.route('/playlistpage')
def playlist_page():
    form_data = flask.request.args
    query = form_data.get("song", "smooth operator")
    results = search_song(query)
    return flask.render_template(
        'playlistpage.html',
        results = results
        )

app.secret_key = os.urandom(12)
app.run(debug=True)
