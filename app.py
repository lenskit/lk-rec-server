from flask import Flask, jsonify, abort, make_response, request
from controller import Controller
from config_reader import ConfigReader

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
    """
    Return the http status code 200.

    Returns:
        The status number 200.
    """
    return jsonify({"status": 200})

@app.route('/preloadmodels', methods=['GET'])
def preload_models():
    """
    Preload the model files into memory, so workers can share them.

    Returns:

    """
    Controller.preload_models()
    return jsonify({"status": 200})

@app.route('/recommendations', methods=['GET', 'POST'])
def recommend_default():
    """
    Get recommendations from the default configured algorithm.

    Returns:
        A list of recommendations with items and scores.
    """
    reader = ConfigReader()
    algo = reader.get_value("default_algorithm")
    return recommend(algo)

def get_param_value(key):
    """First try to get the value from values (query string or form data), if not, from json data. """
    value = request.values.get(key, '')
    if value == '':
        value = request.json.get(key, '')
    return value

# Test local urls:
# http://127.0.0.1:8000/algorithms/popular/recommendations?user_id=2038&num_recs=10
#@app.route('/algorithms/<algo>/recommendations/<int:user_id>/<int:num_recs>', methods=['GET', 'POST'])
@app.route('/algorithms/<algo>/recommendations', methods=['GET', 'POST'])
def recommend(algo):
    """
    Get recommendations using the algorithm and user id sent.

    Args:
        algo: algorithm to be used.
        user_id: user id to get recommendations for.
        num_recs: number of recommendations to return.

    Returns:
        A list of recommendations with items and scores.
    """
    user_id = get_param_value('user_id')
    num_recs = get_param_value('num_recs')

    ctrl = Controller()
    recs = ctrl.get_results_from_model(user_id, num_recs, algo, None)
    return jsonify({'recommendations': recs})
 
 # Test local urls:
 # http://127.0.0.1:5001/algorithms/bias/predictions?user_id=22&items=5,102,203,304,400
 # http://127.0.0.1:5001/algorithms/itemitem/predictions?user_id=22&items=5,102,203,304,400
 # http://127.0.0.1:5001/algorithms/useruser/predictions?user_id=22&items=5,102,203,304,400
 # http://127.0.0.1:5001/algorithms/biasedmf/predictions?user_id=22&items=5,102,203,304,400
 # http://127.0.0.1:5001/algorithms/implicitmf/predictions?user_id=22&items=5,102,203,304,400
 # http://127.0.0.1:5001/algorithms/funksvd/predictions?user_id=22&items=5,102,203,304,400
@app.route('/algorithms/<algo>/predictions', methods=['GET', 'POST'])
def predict(algo):
    """
    Get predictions using the algorithm, user id and items sent.

    Args:
        algo: algorithm to be used.
        user_id: user id to get predictions for.
        items: items to get predictions for.

    Returns:
        A list of predictions with items and scores.
    """
    user_id = int(get_param_value('user_id'))
    items = get_param_value('items')    
    ctrl = Controller()
    items = list(map(int, items.split(',')))

    preds = ctrl.get_results_from_model(user_id, None, algo, items)
    return jsonify({'predictions': preds})

@app.route('/algorithms/<algo>/info', methods=['GET'])
def get_model_info(algo):
    """
    Get the model file information.

    Args:
        algo: algorithm to get the information for.

    Returns:
        Information from the model file such as creation_date, updated_date and size.
    """
    ctrl = Controller()
    return jsonify({'model': ctrl.get_model_info(algo)})

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
        ctrl.upload_model(algo, file) # upload the first entry file
        return jsonify({'result': 200})
    else:
        return jsonify({'result': 'No file sent'})

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