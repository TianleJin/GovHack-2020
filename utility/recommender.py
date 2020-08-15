# pip install pandas
import pandas as pd
DATAPATH = './data/suburb_data.csv'


class Recommender:

    def __init__(self):
        self.db = pd.read_csv(DATAPATH, sep=',')
    
    def recommend(self, diversity, age_diversity, n=10):
        # n = number of recommendations
        # returns postcodes, latitudes, longitudes
        data = self.db[['postcode', 'lat', 'lon', 'diversity_std', 'age_diversity_std']].drop_duplicates(subset='postcode')
        data['metric'] = (data['diversity_std'] - diversity) ** 2 + (data['age_diversity_std'] - age_diversity) ** 2
        locations = data.nsmallest(n, columns='metric')
        return list(locations['postcode']), list(locations['lat']), list(locations['lon'])


if __name__ == '__main__':
    recommender = Recommender()
    print(recommender.recommend(1, 1))
