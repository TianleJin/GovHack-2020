import flask
from flask import send_file, request, redirect, render_template, url_for, flash
import os

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")
    
@app.route('/about_us')
def about_us():
    return render_template("about_us.html")

if __name__ == '__main__':
    app.run(port=os.getenv('PORT', 5000), debug=True)