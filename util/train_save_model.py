import os
import sys
import pandas as pd
import json
import logging
from sqlalchemy import create_engine
from pandas.io import sql
from lenskit.algorithms import basic, als
import lenskit.algorithms.item_knn as iknn
import lenskit.algorithms.user_knn as uknn
import lenskit.algorithms.funksvd as svd
from lenskit.algorithms.implicit import BPR
from lenskit.algorithms import tf as lktf
from pathlib import Path
from binpickle import dump
from lenskit.sharing import sharing_mode
import requests

def get_value(key):
    with open('train_save_model_config.json') as json_data_file:
        data = json.load(json_data_file)
    return data[key]

def get_ratings_from_file():
    directory_path = get_value("data_folder_path")
    ratings_file_name = get_value("ratings_file_name")
    return pd.read_csv(directory_path + ratings_file_name, sep=',', names=['user', 'item', 'rating', 'timestamp'], header=0)

def get_ratings_from_db():
    db_connection = get_value("db_connection")
    conn_string = '{db_engine}{connector}://{user}:{password}@{server}'.format(
        db_engine=db_connection['db_engine'],
        connector=db_connection['connector'],
        user=db_connection['user'],
        password=db_connection['password'],
        server=db_connection['server'])
    db_name = db_connection['database']
    return sql.read_sql("SELECT user, item, rating, timestamp FROM rating;", create_engine(f"{conn_string}/{db_name}?port={db_connection['port']}"))

def get_algo_class(algo):
    if algo == 'popular':
        return basic.Popular()
    elif algo == 'bias':
        return basic.Bias(users=False)
    elif algo == 'topn':
        return basic.TopN(basic.Bias())
    elif algo == 'itemitem':
        return iknn.ItemItem(nnbrs=-1)
    elif algo == 'useruser':
        return uknn.UserUser(nnbrs=5)
    elif algo == 'biasedmf':
        return als.BiasedMF(50, iterations=10)
    elif algo == 'implicitmf':
        return als.ImplicitMF(20, iterations=10)
    elif algo == 'funksvd':
        return svd.FunkSVD(20, iterations=20)
    elif algo == 'tf_bpr':
        return lktf.BPR(20, batch_size=1024, epochs=5, neg_count=2, rng_spec=42)

def get_topn_algo_class(algo):
    if algo == 'popular':
        return basic.Popular()
    elif algo == 'bias':
        return basic.TopN(basic.Bias())
    elif algo == 'itemitem':
        return basic.TopN(iknn.ItemItem(nnbrs=-1, center=False, aggregate='sum'))
    elif algo == 'useruser':
        return basic.TopN(uknn.UserUser(nnbrs=5, center=False, aggregate='sum'))
    elif algo == 'biasedmf':
        return basic.TopN(als.BiasedMF(50, iterations=10))
    elif algo == 'implicitmf':
        return basic.TopN(als.ImplicitMF(20, iterations=10))
    elif algo == 'funksvd':
        return basic.TopN(svd.FunkSVD(20, iterations=20))
    elif algo == 'bpr':
        return basic.TopN(BPR(25))

def create_model(algo, ratings):
    create_top_n_models = get_value("create_top_n_models")
    if create_top_n_models:
        algo_class = get_topn_algo_class(algo)
    else:
        algo_class = get_algo_class(algo)

    if algo_class != None:
        algo_class.fit(ratings)
        return algo_class

def store(data, file_name):
    models_folder_path = get_value("models_folder_path")
    full_file_name = Path(models_folder_path) / file_name

    if full_file_name.exists():
        os.remove(full_file_name)

    if not os.path.exists(models_folder_path):
        os.makedirs(models_folder_path)

    sharingmode = get_value("create_memory_optimized_models")
    if sharingmode:
        with sharing_mode():
            dump(data, full_file_name, mappable=True)
    else:
        dump(data, full_file_name)

def upload_model(algo):
    rec_server_base_url = get_value("rec_server_base_url")
    right_url = f'algorithms/{algo}/modelfile'
    model_name = algo + ".bpk"
    file_path = get_value("models_folder_path") + model_name
    files = {
        'file': open(file_path, 'rb')
    }
    response = requests.put(rec_server_base_url + right_url, files=files)
    return response

def save_models():
    algos = get_value("algorithms")
    if get_value("create_models"):
        from_data_files = get_value("from_data_files") == True
        if from_data_files:
            print('Getting data from file')
            ratings = get_ratings_from_file()
        else:
            print('Getting data from db')
            ratings = get_ratings_from_db()

        for algo in algos:
            algo = algo.strip()
            print(f'Creating model for {algo}')
            model = create_model(algo, ratings)
            if model != None:
                store(model, algo + ".bpk")
                print(f'Model {algo} saved successfully')
            else:
                print(f'Algorithm {algo} not found')

    if get_value("upload_models"):
        print('Uploading models')
        for algo in algos:
            algo = algo.strip()
            print(f'Uploading model for {algo}')
            upload_model(algo)

if __name__ == "__main__":
    save_models()