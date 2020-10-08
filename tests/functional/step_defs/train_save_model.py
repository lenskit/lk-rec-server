import os
import sys
import pandas as pd
import json
import logging
from sqlalchemy import create_engine
from pandas.io import sql
from lenskit.algorithms import basic, als, Predictor, Recommender
import lenskit.algorithms.item_knn as iknn
import lenskit.algorithms.user_knn as uknn
import lenskit.algorithms.funksvd as svd
from lenskit.algorithms.implicit import BPR
from pathlib import Path
from binpickle import dump
from lenskit.sharing import sharing_mode

def get_value(key):
    with open("tests/functional/step_defs/" + 'train_save_model_config.json') as json_data_file:
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
    return sql.read_sql("SELECT userId as user, itemId as item, rating, timestamp FROM ratings;", create_engine(conn_string + "/" + db_name))

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
    algo_class = get_algo_class(algo)
    if algo_class != None:
        algo_class.fit(ratings)
        return algo_class

def store(data, file_name, sharingmode=True):
    models_folder_path = get_value("models_folder_path")
    full_file_name = Path(models_folder_path) / file_name

    if full_file_name.exists():
        os.remove(full_file_name)

    if not os.path.exists(models_folder_path):
        os.makedirs(models_folder_path)

    if sharingmode:
        with sharing_mode():
            dump(data, full_file_name, mappable=True)
    else:
        dump(data, full_file_name)

def save_models(algos, overwrite=False, from_data_files=True):
    if from_data_files:
        logging.info('Getting data from file')
        ratings = get_ratings_from_file()
    else:
        logging.info('Getting data from db')
        ratings = get_ratings_from_db()

    for algo in algos.split(','):
        algo = algo.strip()
        full_file_name = Path(get_value("models_folder_path") + algo + ".bpk")
        if full_file_name.exists() and not overwrite:
            logging.info(f'Model already exists for {algo}. Skipping model creation.')
        else:
            logging.info(f'Creating model for {algo}')
            model = create_model(algo, ratings)
            if model != None:
                store(model, algo + ".bpk", False)
                logging.info(f'Model {algo} saved successfully')
            else:
                logging.info(f'Algorithm {algo} not found')