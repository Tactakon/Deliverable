import flask
import random
import os
from flask import Flask, flash, redirect, render_template, request, session, abort
import logging

from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)

#database boilerplate code
current_dir = os.path.dirname(os.path.abspath(__file__)) #temporary for logging in without database info
basedir = os.path.join(current_dir, "Verge")
my_file_path = os.path.join(basedir, "data", "myfile.txt") 
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
    creator = db.Column(db.Integer, db.ForeignKey('Users.id'))
    listeners_shared_to = db.Column(db.String(1024))
    user = db.relationship("Users", back_populates="playlists")

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

app.secret_key = os.urandom(12)
app.run(debug=True)
