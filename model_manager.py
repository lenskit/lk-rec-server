import os
from pathlib import Path
from binpickle import dump, load, BinPickleFile
from lenskit.sharing import sharing_mode

directory_path = "models"
extension = ".bpk"

def store(data, file_name, sharingmode=True):
    if not file_name.count(extension):
        file_name += extension
    full_file_name = Path(directory_path) / file_name

    if full_file_name.exists():
        os.remove(full_file_name)

    if sharingmode:
        with sharing_mode():
            dump(data, full_file_name, mappable=True)
    else:
        dump(data, full_file_name)


def load(file_name):        
    # for reading also binary mode is important
    if not file_name.count(extension):
        file_name += extension
    full_file_name = Path(directory_path) / file_name
    model = load(full_file_name)
    return model

def load_for_shared_mem(file_name):
    if not file_name.count(extension):
        file_name += extension
    full_file_name = Path(directory_path) / file_name

    binpickle_file = BinPickleFile(full_file_name, direct=True)
    model = binpickle_file.load()
    return model
