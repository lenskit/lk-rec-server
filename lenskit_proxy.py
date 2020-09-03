import math
from lenskit.algorithms import basic, als, Predictor, Recommender
import lenskit.algorithms.item_knn as iknn
import lenskit.algorithms.user_knn as uknn
import lenskit.algorithms.funksvd as svd

# def get_recs(self, user, nr_recs, algo, ratings, items):
#     recs = []
#     algo_class = self.get_algo_class(algo)
#     algo_class.fit(ratings)
#     if isinstance(algo_class, Recommender):
#         df_recs = algo_class.recommend(user, int(nr_recs))
#         for index, row in df_recs.iterrows():
#             recs.append({'item': round(row['item'], 3), 'score': round(row['score'], 3)})
#     elif isinstance(algo_class, Predictor):
#         df_recs = algo_class.predict_for_user(user, items)
#         for index, value in df_recs.iteritems():
#             if not math.isnan(value):
#                 recs.append({'item': index, 'score': round(value, 3)})
#     return recs

def get_recommendations_from_model(model, *args):
    print(args)
    user, nr_recs = args[0][0], args[0][1]
    results = []
    df_recs = model.recommend(user, int(nr_recs))
    for index, row in df_recs.iterrows():
        results.append({'item': row['item'], 'score': row['score']})
    return results

def get_predictions_from_model(model, *args):
    user, items, ratings = args[0][0], args[0][1], args[0][2]
    results = []
    df_preds = model.predict_for_user(user, items, ratings)
    for index, value in df_preds.iteritems():
        if not math.isnan(value):
            results.append({'item': index, 'score': value})
    return results


# def get_algo_class(self, algo):
#     if algo == 'popular':
#         return basic.Popular()
#     elif algo == 'bias':
#         return basic.Bias(users=False)
#     elif algo == 'topn':
#         return basic.TopN(basic.Bias())
#     elif algo == 'itemitem':
#         return iknn.ItemItem(nnbrs=-1)
#     elif algo == 'useruser':
#         return uknn.UserUser(nnbrs=5)
#     elif algo == 'biasedmf':
#         return als.BiasedMF(50, iterations=10)
#     elif algo == 'implicitmf':
#         return als.ImplicitMF(20, iterations=10)
#     elif algo == 'funksvd':
#         return svd.FunkSVD(20, iterations=20)

# def create_model(self, algo, ratings):
#     algo_class = self.get_algo_class(algo)
#     algo_class.fit(ratings)
#     return algo_class