import os
from pathlib import Path
from binpickle import dump, load, BinPickleFile
from lenskit.sharing import sharing_mode
from datetime import datetime
from os import path

directory_path = "lkweb/models"
extension = ".bpk"

def store_model(data, file_name, sharingmode=True):
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


def load_model(file_name):
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

def get_model_file_info(file_name):
    if not file_name.count(extension):
        file_name += extension
    full_file_name = Path(directory_path) / file_name
    creation_date = datetime.utcfromtimestamp(path.getctime(full_file_name))
    updated_date = datetime.utcfromtimestamp(path.getmtime(full_file_name))
    size = path.getsize(full_file_name) / 1000
    return { 
            "creation_date": creation_date.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_date": updated_date.strftime('%Y-%m-%d %H:%M:%S'),
            "size": size
        }