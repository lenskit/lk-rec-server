import os
from flask import Flask, jsonify, abort, make_response, request
from os import path, listdir
from pathlib import Path
from datetime import datetime
from controller import Controller
import config_reader

from functools import wraps
import model_manager
import lenskit_proxy
from lenskit.algorithms import Predictor, Recommender
import db_manager

app = Flask(__name__)

def get_param_value(key):
    """First try to get the value from values (query string or form data), if not, from json data. """
    value = request.values.get(key, '')
    if value == '':
        value = request.json.get(key, '')
    return value

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404    

@app.route('/status', methods=['GET'])
def status():
    """
    Return the http status code 200.

    Returns:
        The status number 200.
    """
    return jsonify({"status": 200})

# @app.route('/preloadmodels', methods=['GET'])
# def preload_models():
#     """
#     Preload the model files into memory, so workers can share them.

#     Returns:

#     """
#     Controller.preload_models()
#     return jsonify({"status": 200})

# @app.route('/recommendations', methods=['GET', 'POST'])
# def recommend_default():
#     """
#     Get recommendations from the default configured algorithm.

#     Returns:
#         A list of recommendations with items and scores.
#     """
#     algo = config_reader.get_value("default_algorithm")
#     return recommend(algo)

# Test local urls:
# http://127.0.0.1:8000/algorithms/popular/recommendations?user_id=2038&num_recs=10
#@app.route('/algorithms/<algo>/recommendations/<int:user_id>/<int:num_recs>', methods=['GET', 'POST'])
# @app.route('/algorithms/<algo>/recommendations', methods=['GET', 'POST'])
# def recommend(algo):
#     """
#     Get recommendations using the algorithm and user id sent.

#     Args:
#         algo: algorithm to be used.
#         user_id: user id to get recommendations for.
#         num_recs: number of recommendations to return.

#     Returns:
#         A list of recommendations with items and scores.
#     """
#     user_id = get_param_value('user_id')
#     num_recs = get_param_value('num_recs')

#     ctrl = Controller()
#     recs = ctrl.get_results_from_model(user_id, num_recs, algo, None)
#     return jsonify({'recommendations': recs})
 
 # Test local urls:
 # http://127.0.0.1:5001/algorithms/bias/predictions?user_id=22&items=5,102,203,304,400
 # http://127.0.0.1:5001/algorithms/itemitem/predictions?user_id=22&items=5,102,203,304,400
 # http://127.0.0.1:5001/algorithms/useruser/predictions?user_id=22&items=5,102,203,304,400
 # http://127.0.0.1:5001/algorithms/biasedmf/predictions?user_id=22&items=5,102,203,304,400
 # http://127.0.0.1:5001/algorithms/implicitmf/predictions?user_id=22&items=5,102,203,304,400
 # http://127.0.0.1:5001/algorithms/funksvd/predictions?user_id=22&items=5,102,203,304,400
# @app.route('/algorithms/<algo>/predictions', methods=['GET', 'POST'])
# def predict(algo):
#     """
#     Get predictions using the algorithm, user id and items sent.

#     Args:
#         algo: algorithm to be used.
#         user_id: user id to get predictions for.
#         items: items to get predictions for.

#     Returns:
#         A list of predictions with items and scores.
#     """
#     user_id = int(get_param_value('user_id'))
#     items = get_param_value('items')    
#     ctrl = Controller()
#     items = list(map(int, items.split(',')))

#     preds = ctrl.get_results_from_model(user_id, None, algo, items)
#     return jsonify({'predictions': preds})

@app.route('/algorithms/<algo>/info', methods=['GET'])
def get_model_info(algo):
    """
    Get the model file information.

    Args:
        algo: algorithm to get the information for.

    Returns:
        Information from the model file such as creation_date, updated_date and size.
    """
    # ctrl = Controller()    
    # return jsonify({'model': ctrl.get_model_info(algo)})
    model_file_dir_path = "models/" + algo + '.bpk'
    creation_date = None
    updated_date = None
    size = 0
    if path.exists(model_file_dir_path):
        creation_date = datetime.utcfromtimestamp(path.getctime(model_file_dir_path)).strftime('%Y-%m-%d %H:%M:%S') 
        updated_date = datetime.utcfromtimestamp(path.getmtime(model_file_dir_path)).strftime('%Y-%m-%d %H:%M:%S')
        size = path.getsize(model_file_dir_path) / 1000
        # dates are in UTC format and size is in KB
        return jsonify({'model': {"creation_date": creation_date, "updated_date": updated_date, "size": size }}) 
    else:
        return jsonify({'model': {}})

@app.route('/algorithms/<algo>/modelfile', methods=['PUT'])
def upload_model(algo):
    """
    Update the model file

    Args:
        algo: algorithm to update the information for.
        file: model file to use 

    Returns:
        A result message of the operation.
    """
    ctrl = Controller()
    keys = list(request.files.keys())
    if len(keys) > 0:
        file = request.files.get(keys[0], None)
        #ctrl.upload_model(algo, file) # upload the first entry file
        
        # save the model file in a temp file
        ts = datetime.now().timestamp()
        temp_file_name = Path(f'models/{algo}_{ts}.bpk')
        file.save(temp_file_name)
        # rename the temp file name
        file_name = Path(f'models/{algo}.bpk')
        os.rename(temp_file_name, file_name)

        return jsonify({'result': 200})
    else:
        return jsonify({'result': 'No file sent'})


def get_recs_params():
     return get_param_value('user_id'), get_param_value('num_recs')

def get_preds_params():
    user_id = int(get_param_value('user_id'))    
    items = list(map(int, get_param_value('items').split(',')))
    ratings = db_manager.get_ratings_for_user(user_id)
    ratings.set_index('item', inplace=True)
    ratings = ratings.iloc[:, 0]
    return user_id, items, ratings

def execute_model(algo, base_class, list_name, func, func_params):
    model = model_manager.load_for_shared_mem(algo)
    if isinstance(model, base_class):
        return jsonify({list_name: func(model, func_params())})
    else:
        return abort(404, description="Model not found")

def get_recommendations_from_default(model, args):
    return lenskit_proxy.get_recommendations_from_model(model, args)

def model_method(name, base_class, list_name, methods=['GET', 'POST']):
	def deco_wrap(func, func_params, default_algo=False):
		@wraps(func)
		def wrapper(algo=None):
			if default_algo:
				algo = config_reader.get_value("default_algorithm")
			return execute_model(algo, base_class, list_name, func, func_params)
		
		if default_algo:
			route = f'/{name}'
		else:
			route = f'/algorithms/<algo>/{name}'
		return app.route(route, methods=methods)(wrapper)
	return deco_wrap

model_method("recommendations", Recommender, 'recommendations')(lenskit_proxy.get_recommendations_from_model, get_recs_params)
model_method("predictions", Predictor, 'predictions')(lenskit_proxy.get_predictions_from_model, get_preds_params)
model_method("recommendations", Recommender, 'recommendations')(get_recommendations_from_default, get_recs_params, True)



# # Save all the algo models to disk
# # http://127.0.0.1:5000/save_models/popular,bias,topn,itemitem,useruser,biasedmf,implicitmf,funksvd
# @app.route('/save_models/<algos>', methods=['GET'])
# def save_models(algos):
#     ctrl = Controller()
#     ctrl.save_models(algos)
#     return jsonify({"result": 200})
    
# print('loading models...')
# Controller.preload_models()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')