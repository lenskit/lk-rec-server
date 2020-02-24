from lenskit_proxy import LenskitProxy
from data_manager import DataManager
from db_manager import DbManager
from model_manager import ModelManager

class Controller:
    def create_db_structure_with_data(self):
        dataManager = DataManager()
        dbManager = DbManager()
        dbManager.create_structure_with_data(dataManager.get_ratings())

    # Get recommendations from data file or database
    def get_recs(self, user_id, nr_recs, algo, items):
        #dataManager = DataManager()
        #ratings = dataManager.get_ratings()
        dbManager = DbManager()
        ratings = dbManager.get_ratings()
        
        lkProxy = LenskitProxy()
        # recs = []
        # for userId in users:
        #     recs.append({'user': userId, 'recs': lkProxy.get_recs(userId, nr_recs, algo, ratings, items)})        
        # return recs
        return lkProxy.get_recs(user_id, nr_recs, algo, ratings, items)
    
    # Get recommendations using a saved model
    def get_recs_using_model(self, user_id, nr_recs, algo, items):
        modelManager = ModelManager()
        lkProxy = LenskitProxy()
        model = modelManager.load(algo)
        return lkProxy.get_recs_from_model(model, user_id, nr_recs,items)

    def save_models(self, algos):
        lkProxy = LenskitProxy()
        #dataManager = DataManager()
        #ratings = dataManager.get_ratings()
        dbManager = DbManager()
        ratings = dbManager.get_ratings()
        print(len(ratings))
        modelManager = ModelManager()
        for algo in algos.split(','):
            model = lkProxy.create_model(algo, ratings)
            modelManager.store(model, algo)
    
    def get_model_info(self, algo):
        return None

    def upload_model(self, algo, data):
        return None

    def preload_models(self):
        return None