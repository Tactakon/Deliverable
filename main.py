import flask
import random
import os
from flask import Flask, flash, redirect, render_template, request, session, abort
import logging

app = flask.Flask(__name__)
#landing page
@app.route("/")
def main():
    #if session.get('logged_in'):
        #goes straight to playlist page if user already logged in
        #return flask.render_template('userPlaylistpage.html')
    #else:
    return flask.render_template('playlistpage.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    return flask.render_template('signup.html')
@app.route('/login', methods=['POST', 'GET'])
def login():
    if flask.request.form['psw'] == 'password' and flask.request.form['email'] == 'admin':
        session['logged_in'] = True
        return flask.render_template('userPlaylistpage.html') #will change to main approute when landingpage has header
    else:
        flask.flash('wrong password!')
        log.info("Username or Password Incorrect")
        return flask.render_template('login.html') #will change to main approute when landingpage has header
app.secret_key = os.urandom(12)
app.run(debug=True)
