import os
from flask import Flask, jsonify, abort, make_response, request
from os import path, listdir
from pathlib import Path
from datetime import datetime
import uuid
import logging

from lenskit.algorithms import Predictor, Recommender

from model_manager import ModelManager
from model_file_manager import load_model, store_model

app = Flask(__name__)
models = ModelManager(app)

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

@app.route('/algorithms/<algo>/info', methods=['GET'])
def get_model_info(algo):
    """
    Get the model file information.

    Args:
        algo: algorithm to get the information for.

    Returns:
        Information from the model file such as creation_date, updated_date and size.
    """
    model_file_dir_path = "models/" + algo + '.bpk'
    creation_date = None
    updated_date = None
    size = 0
    if path.exists(model_file_dir_path):
        logging.info("Getting model information")
        creation_date = datetime.utcfromtimestamp(path.getctime(model_file_dir_path))
        updated_date = datetime.utcfromtimestamp(path.getmtime(model_file_dir_path))
        size = path.getsize(model_file_dir_path) / 1000
        # dates are in UTC format and size is in KB
        return jsonify({'model': {
            "creation_date": creation_date.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_date": updated_date.strftime('%Y-%m-%d %H:%M:%S'),
            "size": size
        }})
    else:
        logging.info("No model found for the algorithm")
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
    keys = list(request.files.keys())
    if len(keys) > 0:
        file = request.files.get(keys[0], None)
        
        logging.info("Create folder if not exists")
        Path("models").mkdir(exist_ok=True)
        
        logging.info("Save the model with a temporary file name")
        temp_model_name = f'{algo}_{uuid.uuid1()}.bpk'
        temp_file_name = Path(f'models/{temp_model_name}')
        file.save(temp_file_name)

        logging.info("Save the model with sharing mode")
        temp_model = load_model(temp_model_name)
        store_model(temp_model, temp_model_name, True)

        logging.info("Rename the temp file name to the actual algorithm name")
        file_name = Path(f'models/{algo}.bpk')
        os.rename(temp_file_name, file_name)

        return jsonify({'result': 200})
    else:
        return jsonify({'result': 'No file sent'})

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')