import flask
import random
import os
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)

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

class Playlists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    password = db.Column(db.String(16))
    songs = db.Column(db.String(10000))
    creator = db.Column(db.Integer(2))
    listeners_shared_to = db.Column(db.String(1024))

#landing page
@app.route("/")
def main():
    #if session.get('logged_in'):
        #header icon change
    #else:
    return flask.render_template('landingpage.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    return flask.render_template('signup.html')
@app.route('/login', methods=['POST', 'GET'])
def login():
    if flask.request.form['psw'] == 'password' and flask.request.form['email'] == 'admin':
        session['logged_in'] = True
    else:
        flask.flash('wrong password!')
        return login()
app.secret_key = os.urandom(12)
app.run(debug=True)
