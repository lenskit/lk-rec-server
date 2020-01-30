import pickle

class ModelManager:

    def __init__(self):
        self.directory_path = "files/"

    def store(self, data, file_name):
        # Its important to use binary mode
        if not file_name.count(".pickle"):
            file_name += ".pickle"
        data_file = open(self.directory_path + file_name, 'ab') 
        
        # source, destination 
        pickle.dump(data, data_file)
        data_file.close()

    def load(self, file_name):        
        # for reading also binary mode is important
        if not file_name.count(".pickle"):
            file_name += ".pickle"
        data_file = open(self.directory_path + file_name, 'rb')      
        model = pickle.load(data_file)
        data_file.close()
        return model
