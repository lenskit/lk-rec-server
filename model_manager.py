import os
import pickle

class ModelManager:

    def __init__(self):
        self.directory_path = "files/"

    def store(self, data, file_name):
        # Its important to use binary mode
        if not file_name.count(".pickle"):
            file_name += ".pickle"
        full_file_name = self.directory_path + file_name

        if os.path.exists(full_file_name):
            os.remove(full_file_name)

        data_file = open(full_file_name, 'ab') 
        
        # source, destination 
        pickle.dump(data, data_file)
        data_file.close()

    def load(self, file_name):        
        # for reading also binary mode is important
        if not file_name.count(".pickle"):
            file_name += ".pickle"
        full_file_name = self.directory_path + file_name
        data_file = open(full_file_name, 'rb')      
        model = pickle.load(data_file)
        data_file.close()
        return model
