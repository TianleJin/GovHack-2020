import flask
import requests
from flask import send_file, request, redirect, render_template, url_for, flash, jsonify
import os
from utility import recommender as ML
import json

app = flask.Flask(__name__)
recommender = ML.Recommender()

with open('ssc_codes.json') as json_file:
    data = json.load(json_file)
    ssc_id = []
    postcode_id = []
    for p in data['data']:
        ssc_id.append(p['id'])
        postcode_id.append(p['postcode'])
    
    print(postcode_id)
    lookup_code = zip(ssc_id, postcode_id)
    print(lookup_code)

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
    lat, lng, population, suburb, postcodes, cultural_diversity, age_diversity = recommender.recommend(float(cultural_diversity_amount) / 100, float(age_diversity_amount) / 100, n=5)
    print(lat, lng, population, suburb, cultural_diversity, age_diversity)

    ssc_codes = [ssc_id[postcode_id.index(str(postcode))] for postcode in postcodes]
    data_calls = ["https://gis-app-cdn.prod.myvictoria.vic.gov.au/geoserver/myvic/ows?service=WFS&version=1.0.0&outputFormat=application%2Fjson&request=GetFeature&typeName=myvic:demographics_suburb&CQL_FILTER=ssc_code=%27" + ssc_code + "%27" for ssc_code in ssc_codes]
    data=[]
    for info in data_calls:
        response = requests.get(info)
        data.append(response.json())

    return render_template("detail.html", lat=lat, lng=lng, population = population, suburb = json.dumps(suburb), cultural_diversity = cultural_diversity, age_diversity = age_diversity, data_calls=data_calls)

if __name__ == '__main__':
    app.run(port=os.getenv('PORT', 5000), debug=True)