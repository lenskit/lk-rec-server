import os
from pathlib import Path
from binpickle import dump, load, BinPickleFile
from lenskit.sharing import sharing_mode

class ModelManager:

    def __init__(self):
        self.directory_path = "models"
        self.extension = ".bpk" #".pickle"

    def store(self, data, file_name):
        if not file_name.count(self.extension):
            file_name += self.extension

#        full_file_name = self.directory_path + file_name
        full_file_name = Path(self.directory_path) / file_name

        # if os.path.exists(full_file_name):
        #     os.remove(full_file_name)
        if full_file_name.exists():
            os.remove(full_file_name)

        # with sharing_mode():
        #     dump(data, full_file_name, mappable=True)
        dump(data, full_file_name)

    def load(self, file_name):        
        # for reading also binary mode is important
        if not file_name.count(self.extension):
            file_name += self.extension
        full_file_name = Path(self.directory_path) / file_name
        # data_file = open(full_file_name, 'rb')      
        # model = pickle.load(data_file)
        # data_file.close()
        model = load(full_file_name)
        return model

    def load_for_shared_mem(self, file_name):
        if not file_name.count(self.extension):
            file_name += self.extension
        full_file_name = Path(self.directory_path) / file_name

        binpickle_file = BinPickleFile(full_file_name, direct=True)
        model = binpickle_file.load()
        return model
