import sys
import os
import logging
import math
from functools import wraps
from flask import request, jsonify
from os import path
from datetime import datetime
from pathlib import Path
import uuid
import logging
from .model_file_manager import load_for_shared_mem, get_model_file_info, load_model, store_model
from .db_manager import get_ratings_for_user

class ModelManager:
    models_cache = {}
    model_directory_path = "lkweb/models" 

    def __init__(self, app):
        self.app = app

    def get_model_info(self, algo):
        model_file_dir_path = f'{ModelManager.model_directory_path}/{algo}.bpk' 
        creation_date = None
        updated_date = None
        size = 0
        if path.exists(model_file_dir_path):
            logging.info("Getting model information")
            creation_date = datetime.utcfromtimestamp(path.getctime(model_file_dir_path))
            updated_date = datetime.utcfromtimestamp(path.getmtime(model_file_dir_path))
            size = path.getsize(model_file_dir_path) / 1000
            # dates are in UTC format and size is in KB
            return jsonify({'model': {
                "creation_date": creation_date.strftime('%Y-%m-%d %H:%M:%S'),
                "updated_date": updated_date.strftime('%Y-%m-%d %H:%M:%S'),
                "size": size
            }})
        else:
            logging.info("No model found for the algorithm")
            return jsonify({'model': {}})        

    def upload_model(self, algo):
        keys = list(request.files.keys())
        if len(keys) > 0:
            file = request.files.get(keys[0], None)
            
            logging.info("Create folder if not exists")
            Path(ModelManager.model_directory_path).mkdir(exist_ok=True)
            
            logging.info("Save the model with a temporary file name")
            temp_model_name = f'{algo}_{uuid.uuid1()}.bpk'
            temp_file_name = Path(f'{ModelManager.model_directory_path}/{temp_model_name}')
            file.save(temp_file_name)

            logging.info("Save the model with sharing mode")
            temp_model = load_model(temp_model_name)
            store_model(temp_model, temp_model_name, True)

            logging.info("Rename the temp file name to the actual algorithm name")
            file_name = Path(f'{ModelManager.model_directory_path}/{algo}.bpk')
            os.rename(temp_file_name, file_name)

            return jsonify({'result': 200})
        else:
            return jsonify({'result': 'No file sent'})

    def get_db_ratings(self, user_id):
        ratings = get_ratings_for_user(user_id, self.app.config)
        if len(ratings) > 0:
            ratings.set_index('item', inplace=True)
            return ratings.iloc[:, 0]
        else:
            return None

    def get_param_value(self, key, *args):
        """First try to get the value from values (query string or form data), if not, from json data. """
        value = request.values.get(key, '')
        if value == '':
            value = request.json.get(key, '')
        return value
    
    def get_recs_params(self, *args):
        user_id = self.get_param_value('user_id')
        return user_id, self.get_param_value('num_recs'), self.get_db_ratings(user_id)

    def get_preds_params(self):
        user_id = int(self.get_param_value('user_id'))    
        items = list(map(int, self.get_param_value('items').split(',')))
        return user_id, items, self.get_db_ratings(user_id)

    def get_recommendations_from_model(self, model, *args):
        user = None
        try:
            user, nr_recs, ratings = args[0][0], args[0][1], args[0][2]
            results = []
            df_recs = model.recommend(int(user), int(nr_recs), ratings=ratings)
            for index, row in df_recs.iterrows():
                results.append({'item': row['item'], 'score': row['score']})
            return results
        except:        
            logging.error(f"Unexpected recs error for user: {user}. Error: {sys.exc_info()[0]}")
            raise
    
    def get_predictions_from_model(self, model, *args):
        user, items = None, None
        try:
            user, items, ratings = args[0][0], args[0][1], args[0][2]
            results = []
            df_preds = model.predict_for_user(user, items, ratings)
            for index, value in df_preds.iteritems():
                if not math.isnan(value):
                    results.append({'item': index, 'score': value})
            return results
        except:
            logging.error(f"Unexpected preds error for user: {user}, with items: {items}. Error: {sys.exc_info()[0]}")
            raise

    def get_worst_predictions_from_model(self, model, *args):
        user, items = None, None
        try:
            user, items, ratings = args[0][0], args[0][1], args[0][2]
            results = []
            df_preds = model.predict_for_user(user, items, ratings)
            for index, value in df_preds.iteritems():
                if not math.isnan(value):
                    results.append({'item': index, 'score': value})
            results = sorted(results, key = lambda i: i['score'])
            return results
        except:
            logging.error(f"Unexpected preds error for user: {user}, with items: {items}. Error: {sys.exc_info()[0]}")
            raise

    @classmethod
    def get_recommendations_from_default(model, *args):
        return ModelManager.get_recommendations_from_model(model, *args)

    def get_model(self, algo):
        if algo not in ModelManager.models_cache:
            logging.info(f'Adding algo {algo} to cache')
            model = load_for_shared_mem(algo)
            info = get_model_file_info(algo)
            ModelManager.models_cache[algo] = { "model": model, "info": info }
            return model
        else:
            # check the modified datetime of the model to see if we need to reload it.
            logging.info(f'Reading algo {algo} from cache')
            model_data = ModelManager.models_cache[algo]
            info = get_model_file_info(algo)
            if model_data['info']['updated_date'] != info['updated_date']:
                logging.info(f'Updating algo {algo} in cache')
                model = load_for_shared_mem(algo)
                ModelManager.models_cache[algo] = { "model": model, "info": info }
            return ModelManager.models_cache[algo]['model']

    def execute_model(self, algo, base_class, get_data_func, get_params_func):
        logging.info("Loading the model")
        model = self.get_model(algo)
        if isinstance(model, base_class):
            logging.info("Executing the model")
            return get_data_func(model, get_params_func())
        # else:
        #     return abort(404, description="Model not found") 

    def model_method(self, name, base_class, get_data_func, get_params_func, default_algo=False, methods=['GET', 'POST']):
        def deco_wrap(func):
            @wraps(func)
            def wrapper(algo=None):
                if default_algo:
                    algo = self.app.config["DEFAULT_ALGORITHM"]
                return func(self.execute_model(algo, base_class, get_data_func, get_params_func))
            
            if default_algo:
                route = f'/{name}'
            else:
                route = f'/algorithms/<algo>/{name}'
            return self.app.route(route, methods=methods)(wrapper)
        return deco_wrap   