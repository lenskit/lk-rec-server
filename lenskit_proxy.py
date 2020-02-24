import math
from lenskit.algorithms import basic, als, Predictor, Recommender
import lenskit.algorithms.item_knn as iknn
import lenskit.algorithms.user_knn as uknn
import lenskit.algorithms.funksvd as svd

class LenskitProxy:
    def get_recs(self, user, nr_recs, algo, ratings, items):
        recs = []
        algo_class = self.get_algo_class(algo)
        algo_class.fit(ratings)
        if isinstance(algo_class, Recommender):
            df_recs = algo_class.recommend(user, int(nr_recs))
            for index, row in df_recs.iterrows():
                recs.append({'item': round(row['item'], 3), 'score': round(row['score'], 3)})
        elif isinstance(algo_class, Predictor):
            df_recs = algo_class.predict_for_user(user, items)
            for index, value in df_recs.iteritems():
                if not math.isnan(value):
                    recs.append({index : round(value, 3)})
        return recs

    def get_recs_from_model(self, model, user, nr_recs, items):
        recs = []
        if isinstance(model, Recommender):
            df_recs = model.recommend(user, int(nr_recs))
            for index, row in df_recs.iterrows():
                recs.append({'item': round(row['item'], 3), 'score': round(row['score'], 3)})
        elif isinstance(model, Predictor):
            df_recs = model.predict_for_user(user, items)
            for index, value in df_recs.iteritems():
                if not math.isnan(value):
                    recs.append({index : round(value, 3)})
        return recs

    def get_algo_class(self, algo):
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
    
    def create_model(self, algo, ratings):
        algo_class = self.get_algo_class(algo)
        algo_class.fit(ratings)
        return algo_class