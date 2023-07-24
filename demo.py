from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route("/hello")
def intro():
    return "Hello World! Welcome to HC CAD Session"


@app.route("/")
def default():
    return "Default route"


@app.route("/hello/<string:track>") #url binding
def welcome(track):
    return f"Welcome to Bootcamp {track} 1"

@app.route("/something")
def something():
    return "Hello World! This is a new Route"


if __name__ == "__main__":
    app.run(debug = True)