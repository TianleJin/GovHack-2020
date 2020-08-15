# pip install pandas
import pandas as pd
DATAPATH = './data/suburb_data.csv'


class Recommender:

    def __init__(self):
        self.db = pd.read_csv(DATAPATH, sep=',')
    
    def recommend(self, diversity, age_diversity, n=10):
        print(type(diversity),diversity,type(age_diversity),age_diversity)
        # n = number of recommendations
        # returns postcodes, latitudes, longitudes
        data = self.db[['postcode', 'lat', 'lon', 'diversity_std', 'age_diversity_std', 'suburb', 'tot_P']].drop_duplicates(subset='postcode')
        data['metric'] = (data['diversity_std'] - diversity) ** 2 + (data['age_diversity_std'] - age_diversity) ** 2
        locations = data.nsmallest(n, columns='metric')
        return list(locations['lat']), list(locations['lon']), list(locations['tot_P']), list(locations['suburb']), list(locations['diversity_std']), list(locations['age_diversity_std'])


if __name__ == '__main__':
    recommender = Recommender()
    print(recommender.recommend(1, 1))
