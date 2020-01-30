from lenskit_proxy import LenskitProxy
from data_manager import DataManager
from db_manager import DbManager
from model_manager import ModelManager

class Controller:
    def create_db_structure_with_data(self):
        dataManager = DataManager()
        dbManager = DbManager()
        dbManager.create_structure_with_data(dataManager.get_ratings())

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
    
    def save_models(self, algos):
        lkProxy = LenskitProxy()
        #dataManager = DataManager()
        #ratings = dataManager.get_ratings()
        dbManager = DbManager()
        ratings = dbManager.get_ratings()
        modelManager = ModelManager()
        for algo in algos.split(','):
            model = lkProxy.create_model(algo, ratings)
            modelManager.store(model, algo)