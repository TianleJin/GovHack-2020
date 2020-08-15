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

@app.route('/handle_data', methods=['POST'])
def handle_data():
    cultural_diversity_amount = request.form['cultureDiversity']
    age_diversity_amount = request.form['ageDiversity']

    # your code
    # return a response
    print('Culture: ', cultural_diversity_amount)
    print('Age: ', age_diversity_amount)

    # ADD ML Code here
    # Inputs: cultural diversity, age_diversity_amount
    # Output: List of 5 top recommendations (coordinates, postcode, suburb name, diversity rankings)

    lat = [-37.814563, -37.81664, -37.806255, -37.837324, -37.822262]
    lng = [144.970267, 144.987811, 144.941123, 144.976335, 144.954856]

    return render_template("detail.html", lat=lat, lng=lng)

if __name__ == '__main__':
    app.run(port=os.getenv('PORT', 5000), debug=True)