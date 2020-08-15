import flask
from flask import send_file, request, redirect, render_template, url_for, flash
import os

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")
    
@app.route('/detail')
def detail():
    return render_template("detail.html")

if __name__ == '__main__':
    app.run(port=os.getenv('PORT', 5000), debug=True)