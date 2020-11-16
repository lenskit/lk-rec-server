import os
import tensorflow as tf

from flask import Flask, jsonify
from lenskit.algorithms import Predictor, Recommender
from lkweb.model_manager import ModelManager

app = Flask(__name__)
models = ModelManager(app)
app.config.from_pyfile('./config.cfg')

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
    print(f"get_inter_op_parallelism_threads: {tf.config.threading.get_inter_op_parallelism_threads()}")
    print(f"get_intra_op_parallelism_threads: {tf.config.threading.get_intra_op_parallelism_threads()}")
    print(f"NUMBA_NUM_THREADS: {os.getenv('NUMBA_NUM_THREADS')}")
    print(f"MKL_NUM_THREADS: {os.getenv('MKL_NUM_THREADS')}")
    print(f"OMP_NUM_THREADS: {os.getenv('OMP_NUM_THREADS')}")
    return jsonify({"status": 200})

@app.route('/algorithms/<algo>/info', methods=['GET'])
def get_model_info(algo):
    """
    Get the model file information.

    Args:
        algo: algorithm to get the information for.

    Returns:
        Information from the model file such as creation_date, updated_date and size.
    """
    return models.get_model_info(algo)


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
    return models.upload_model(algo)

@models.model_method("recommendations", Recommender, models.get_recommendations_from_model, models.get_recs_params)
def recommend(results):
    """
    Get recommendations using the algorithm and user id sent.
    Args:
        algo: algorithm to be used.
        user_id: user id to get recommendations for.
        num_recs: number of recommendations to return.
    Returns:
        A list of recommendations with items and scores.
    """    
    return jsonify({"recommendations": results})

@models.model_method("predictions", Predictor, models.get_predictions_from_model, models.get_preds_params)
def get_predictions(results):
    """
    Get predictions using the algorithm, user id and items sent.
    Args:
        algo: algorithm to be used.
        user_id: user id to get predictions for.
        items: items to get predictions for.
    Returns:
        A list of predictions with items and scores.
    """
    return jsonify({"predictions": results})

@models.model_method("recommendations", Recommender, models.get_recommendations_from_default, models.get_recs_params, True)
def recommend_default(results):
    """
    Get recommendations from the default configured algorithm.
    Returns:
        A list of recommendations with items and scores.
    """
    return jsonify({"recommendations": results})

@models.model_method("worst_predictions", Predictor, models.get_worst_predictions_from_model, models.get_preds_params)
def get_worst_predictions(results):
    """
    Get worst predictions using the algorithm, user id and items sent.
    Args:
        algo: algorithm to be used.
        user_id: user id to get predictions for.
        items: items to get predictions for.
    Returns:
        A list of predictions with items and scores.
    """
    return jsonify({"predictions": results})

# set env variables:
def set_performance_vars():
    os.environ['NUMBA_NUM_THREADS'] = "1"
    os.environ['MKL_NUM_THREADS'] = "1"
    os.environ['OMP_NUM_THREADS'] = "1"
    tf.config.threading.set_inter_op_parallelism_threads(1)
    tf.config.threading.set_intra_op_parallelism_threads(1)

set_performance_vars()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')