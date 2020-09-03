import os
from os import path, listdir
from datetime import datetime
from pathlib import Path
import lenskit_proxy
import db_manager
import model_manager

class Controller:
    models = {}
    
    # Get recommendations using a saved model    
    def get_results_from_model(self, user_id, nr_recs, algo, items):
        ratings = db_manager.get_ratings_for_user(user_id)
        ratings.set_index('item', inplace=True)
        ratings = ratings.iloc[:, 0]
        model = Controller.models.get(algo, None)
        if model == None:
            print('\033[1;31;47m Model not loaded in memory!!! Model will be load now for this request. \033[0m')
            model = model_manager.load_for_shared_mem(algo)
            Controller.models[algo] = model
        
        return lenskit_proxy.get_results_from_model(model, user_id, nr_recs, items, ratings)
    
    def get_model_info(self, algo):
        model_file_dir_path = "models/" + algo + '.bpk'
        creation_date = None
        updated_date = None
        size = 0
        if path.exists(model_file_dir_path):
            creation_date = datetime.utcfromtimestamp(path.getctime(model_file_dir_path)).strftime('%Y-%m-%d %H:%M:%S') 
            updated_date = datetime.utcfromtimestamp(path.getmtime(model_file_dir_path)).strftime('%Y-%m-%d %H:%M:%S')
            size = path.getsize(model_file_dir_path) / 1000
            # dates are in UTC format and size is in KB
            return {"creation_date": creation_date, "updated_date": updated_date, "size": size }
        else:
            return {}
        
    def upload_model(self, algo, file):
        # save the model file in a temp file
        ts = datetime.now().timestamp()
        temp_file_name = Path(f'models/{algo}_{ts}.bpk')
        file.save(temp_file_name)
        # rename the temp file name
        file_name = Path(f'models/{algo}.bpk')
        os.rename(temp_file_name, file_name)
    
    @staticmethod
    def preload_models():
        model_file_dir_path = "models/"
        for filename in listdir(model_file_dir_path):
            if not filename.startswith('.'):
                key = filename.split('.')[0]
                Controller.models[key] = model_manager.load_for_shared_mem(filename)

    # def save_models(self, algos):
    #     lkProxy = LenskitProxy()
    #     dbManager = DbManager()
    #     ratings = dbManager.get_ratings()
    #     for algo in algos.split(','):
    #         model = lkProxy.create_model(algo, ratings)
    #         model_manager.store(model, algo)