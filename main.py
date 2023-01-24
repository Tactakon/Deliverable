import flask
import random

app = flask.Flask(__name__)

@app.route("/")
def index():
    return 'Collaborative DJing WebApp!'

if __name__ == '__main__':
    app.run(debug=True)