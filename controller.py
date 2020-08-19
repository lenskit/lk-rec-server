from os import path, listdir
from datetime import datetime
from lenskit_proxy import LenskitProxy
from db_manager import DbManager
from model_manager import ModelManager

class Controller:
    models = {}
    
    # Get recommendations using a saved model
    def get_results_from_model(self, user_id, nr_recs, algo, items):
        modelManager = ModelManager()
        lkProxy = LenskitProxy()
        dbManager = DbManager()
        ratings = dbManager.get_ratings_for_user(user_id)
        ratings.set_index('item', inplace=True)
        ratings = ratings.iloc[:, 0]
        model = Controller.models.get(algo, None)
        if model == None:
            print('\033[1;31;47m Model not loaded in memory!!! Model will be load now for this request. \033[0m')
            model = modelManager.load_for_shared_mem(algo)      
            Controller.models[algo] = model
        
        return lkProxy.get_results_from_model(model, user_id, nr_recs, items, ratings)
    
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
        file_name = path.join('models/' + algo + '.bpk')
        file.save(file_name)

    @staticmethod
    def preload_models():
        model_file_dir_path = "models/"
        modelManager = ModelManager()
        for filename in listdir(model_file_dir_path):
            if not filename.startswith('.'):
                key = filename.split('.')[0]
                Controller.models[key] = modelManager.load_for_shared_mem(filename)
                # modelManager.load_for_shared_mem(filename)

    def save_models(self, algos):
        lkProxy = LenskitProxy()
        dbManager = DbManager()
        ratings = dbManager.get_ratings()
        modelManager = ModelManager()
        for algo in algos.split(','):
            model = lkProxy.create_model(algo, ratings)
            modelManager.store(model, algo)