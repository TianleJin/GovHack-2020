import flask
from flask import send_file, request, redirect, render_template, url_for, flash
import os
from utility import recommender as ML

app = flask.Flask(__name__)
recommender = ML.Recommender()

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

    # Inputs: cultural diversity, age_diversity_amount
    # Output: List of 5 top recommendations (coordinates, postcode, suburb name, diversity rankings)
    postcode, lat, lng = recommender.recommend(float(cultural_diversity_amount) / 100, float(age_diversity_amount) / 100, n=5)

    return render_template("detail.html", postcode=postcode, lat=lat, lng=lng)

if __name__ == '__main__':
    app.run(port=os.getenv('PORT', 5000), debug=True)