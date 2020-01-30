import pandas as pd

class DataManager:
    def __init__(self):
        self.directory_path = "data/"
        self.ratings_file_name = "u.data"
    
    def get_ratings(self):
        # TODO: See how to handle the format for other files
        return pd.read_csv(self.directory_path + self.ratings_file_name, sep='\t', names=['user', 'item', 'rating', 'timestamp'])