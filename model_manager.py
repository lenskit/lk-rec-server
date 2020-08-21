import os
from pathlib import Path
from binpickle import dump, load, BinPickleFile
from lenskit.sharing import sharing_mode

class ModelManager:

    def __init__(self):
        self.directory_path = "models"
        self.extension = ".bpk"

    def store(self, data, file_name, sharingmode=True):
        if not file_name.count(self.extension):
            file_name += self.extension
        full_file_name = Path(self.directory_path) / file_name

        if full_file_name.exists():
            os.remove(full_file_name)

        if sharingmode:
            with sharing_mode():
                dump(data, full_file_name, mappable=True)
        else:
            dump(data, full_file_name)


    def load(self, file_name):        
        # for reading also binary mode is important
        if not file_name.count(self.extension):
            file_name += self.extension
        full_file_name = Path(self.directory_path) / file_name
        model = load(full_file_name)
        return model

    def load_for_shared_mem(self, file_name):
        if not file_name.count(self.extension):
            file_name += self.extension
        full_file_name = Path(self.directory_path) / file_name

        binpickle_file = BinPickleFile(full_file_name, direct=True)
        model = binpickle_file.load()
        return model
