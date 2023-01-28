import flask
import random
import os
from flask import Flask, flash, redirect, render_template, request, session, abort

app = flask.Flask(__name__)

@app.route("/")
def main():
    #if not session.get('logged_in'):
        #return render_template('login.html')
    #else:
    return flask.render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if flask.request.form['psw'] == 'password' and flask.request.form['email'] == 'admin':
        session['logged_in'] = True
    else:
        flask.flash('wrong password!')
        return main()
app.secret_key = os.urandom(12)
app.run(debug=True)