import math
import sys
from lenskit.algorithms import basic, als, Predictor, Recommender
import lenskit.algorithms.item_knn as iknn
import lenskit.algorithms.user_knn as uknn
import lenskit.algorithms.funksvd as svd

def get_recommendations_from_model(model, *args):
    try:
        user, nr_recs = args[0][0], args[0][1]
        results = []
        df_recs = model.recommend(user, int(nr_recs))
        for index, row in df_recs.iterrows():
            results.append({'item': row['item'], 'score': row['score']})
        return results
    except:
        print(f"Unexpected recs error for user: {user}. Error: {sys.exc_info()[0]}")
        raise

def get_predictions_from_model(model, *args):
    try:
        user, items, ratings = args[0][0], args[0][1], args[0][2]
        results = []
        df_preds = model.predict_for_user(user, items, ratings)
        for index, value in df_preds.iteritems():
            if not math.isnan(value):
                results.append({'item': index, 'score': value})
        return results
    except:
        print(f"Unexpected preds error for user: {user}, with items: {items}. Error: {sys.exc_info()[0]}")
        raise
