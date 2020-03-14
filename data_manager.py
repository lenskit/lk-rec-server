import pandas as pd

class DataManager:
    def __init__(self):
        self.directory_path = "data/"
        self.ratings_file_name = "ratings.csv"
        self.movies_file_name = "movies.csv"
        self.links_file_name = "links.csv"
    
    def get_ratings(self):
        # TODO: See how to handle the format for other files
        #return pd.read_csv(self.directory_path + self.ratings_file_name, sep=',', names=['user', 'item', 'rating', 'timestamp'])
        return pd.read_csv(self.directory_path + self.ratings_file_name, sep=',')
    
    def get_movies(self):
        return pd.read_csv(self.directory_path + self.movies_file_name, sep=',')

    def get_links(self):
        return pd.read_csv(self.directory_path + self.links_file_name, sep=',')