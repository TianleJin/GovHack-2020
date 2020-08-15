# pip install pandas
import pandas as pd
DATAPATH = './data/suburb_data.csv'


class Database:

    def __init__(self):
        self.db = pd.read_csv(DATAPATH, sep=',')
    
    def calculate_age_diversity(self):
        labels = [label for label in self.db.columns if label.startswith('age')]
        data = self.db[labels]
        total = data.sum(axis=1)
        for label in labels:
            data[label] = data[label] / total
            data[label] = data[label] ** 2
        age_diversity = 1 - data.sum(axis=1)
        self.db['age_diversity_std'] = (age_diversity - age_diversity.min()) / (age_diversity.max() - age_diversity.min())

    def save(self):
        self.db.to_csv(DATAPATH, sep=',')


if __name__ == '__main__':
    db = Database()
    db.calculate_age_diversity()
    db.save()