import sys
import logging
import math
from functools import wraps
from flask import jsonify, request
from model_file_manager import load_for_shared_mem
from config_reader import get_value
from db_manager import get_ratings_for_user

class ModelManager:

    def __init__(self, app):
        self.app = app

    def get_db_ratings(self, user_id):
        ratings = get_ratings_for_user(user_id)
        ratings.set_index('item', inplace=True)
        return ratings.iloc[:, 0]

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

    @classmethod
    def get_recommendations_from_default(model, *args):
        return ModelManager.get_recommendations_from_model(model, *args)

    def execute_model(self, algo, base_class, get_data_func, get_params_func):
        logging.info("Loading the model")        
        model = load_for_shared_mem(algo)
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
                    algo = get_value("default_algorithm")
                return func(self.execute_model(algo, base_class, get_data_func, get_params_func))
            
            if default_algo:
                route = f'/{name}'
            else:
                route = f'/algorithms/<algo>/{name}'
            return self.app.route(route, methods=methods)(wrapper)
        return deco_wrap   