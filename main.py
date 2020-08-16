import flask
import requests
from flask import send_file, request, redirect, render_template, url_for, flash, jsonify
import os
from utility import recommender as ML
import json

app = flask.Flask(__name__)
recommender = ML.Recommender()

# For Heroku
app.secret_key = os.environ.get('MAPS_SECRET_KEY')

with open('ssc_codes.json') as json_file:
    data = json.load(json_file)
    ssc_id = []
    postcode_id = []
    for p in data['data']:
        ssc_id.append(p['id'])
        postcode_id.append(p['postcode'])

    lookup_code = zip(ssc_id, postcode_id)

@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")
    
@app.route('/detail')
def detail():
    return render_template("detail.html")

@app.route('/handle_data', methods=['POST'])
def handle_data():
    cultural_diversity_amount = float(request.form['cultureDiversity'])/100
    age_diversity_amount = float(request.form['ageDiversity'])/100
    rent_amount = int(request.form['rent-value'])/4
    population_choice = float(request.form['population'])/100

    # your code
    # return a response
    print('Culture: ', cultural_diversity_amount)
    print('Age: ', age_diversity_amount)

    # Inputs: cultural diversity, age_diversity_amount
    # Output: List of 5 top recommendations (coordinates, postcode, suburb name, diversity rankings)
    lat_, lng_, population_, suburb_, postcodes_, cultural_diversity_, age_diversity_ = recommender.recommend(cultural_diversity_amount, age_diversity_amount, population_choice, n=20)
    lat, lng, population, suburb, cultural_diversity, age_diversity = [],[],[],[],[],[]

    indexes = []
    ssc_codes = []
    for i in range(len(postcodes_)):
        if str(postcodes_[i]) in postcode_id:
            ssc_codes.append(ssc_id[postcode_id.index(str(postcodes_[i]))])
            indexes.append(i)
        if len(ssc_codes) == 5:
            break

    print(ssc_codes)

    for i in indexes:
        lat.append(lat_[i])
        lng.append(lng_[i])
        population.append(population_[i])
        suburb.append(suburb_[i])
        cultural_diversity.append(cultural_diversity_[i])
        age_diversity.append(age_diversity_[i])

    print(lat,lng,population,suburb,cultural_diversity,age_diversity)

    data_calls = ["https://gis-app-cdn.prod.myvictoria.vic.gov.au/geoserver/myvic/ows?service=WFS&version=1.0.0&outputFormat=application%2Fjson&request=GetFeature&typeName=myvic:demographics_suburb&CQL_FILTER=ssc_code=%27" + str(ssc_code) + "%27" for ssc_code in ssc_codes]
    data=[]
    for info in data_calls:
        response = requests.get(info)
        print(response.json())
        data.append(response.json())

    return render_template("detail.html", userInfo=[cultural_diversity_amount, age_diversity_amount, rent_amount, population_choice], lat=lat, lng=lng, population = population, suburb = json.dumps(suburb), cultural_diversity = cultural_diversity, age_diversity = age_diversity, data_calls=data_calls)

if __name__ == '__main__':
    app.run(port=os.getenv('PORT', 5000), debug=True)