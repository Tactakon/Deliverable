import flask
import random
import os
from flask import Flask, flash, redirect, render_template, request, session, abort

app = flask.Flask(__name__)
#landing page
@app.route("/")
def main():
    #if session.get('logged_in'):
        #header icon change
    #else:
    return flask.render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    return flask.render_template('signup.html')
@app.route('/login', methods=['POST', 'GET'])
def login():
    if flask.request.form['psw'] == 'password' and flask.request.form['email'] == 'admin':
        session['logged_in'] = True
        return flask.render_template('playlist.html')
    else:
        flask.flash('wrong password!')
        return login()
app.secret_key = os.urandom(12)
app.run(debug=True)