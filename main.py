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

    # your code
    # return a response
    print('Culture: ', cultural_diversity_amount)
    print('Age: ', age_diversity_amount)

    # Inputs: cultural diversity, age_diversity_amount
    # Output: List of 5 top recommendations (coordinates, postcode, suburb name, diversity rankings)
    lat, lng, population, suburb, cultural_diversity, age_diversity = recommender.recommend(float(cultural_diversity_amount) / 100, float(age_diversity_amount) / 100, n=5)

    return render_template("detail.html", lat=lat, lng=lng, population = population, suburb = suburb, cultural_diversity = cultural_diversity, age_diversity = age_diversity)

if __name__ == '__main__':
    app.run(port=os.getenv('PORT', 5000), debug=True)