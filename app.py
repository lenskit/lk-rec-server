from flask import Flask, jsonify, abort, make_response, request
from controller import Controller
from config_reader import ConfigReader

app = Flask(__name__)

@app.route('/preloadmodels', methods=['GET'])
def preload_models():
    #ctrl = Controller()
    Controller.preload_models()
    return jsonify({"result": 'ok'})

# Default algo path:
# 	/recommendations
@app.route('/recommendations', methods=['GET', 'POST'])
def recommend_default():
    reader = ConfigReader()
    algo = reader.get_value("default_algorithm")
    return recommend(algo)

def get_param_value(key):
    # first try to get the value from values (query string or form data), if not, from json data
    value = request.values.get(key, '')
    if value == '':
        value = request.json.get(key, '')
    return value

# Test local urls:
# http://127.0.0.1:8000/algorithms/popular/recommendations?user_id=2038&num_recs=10
#@app.route('/algorithms/<algo>/recommendations/<int:user_id>/<int:num_recs>', methods=['GET', 'POST'])
@app.route('/algorithms/<algo>/recommendations', methods=['GET', 'POST'])
def recommend(algo):
    user_id = get_param_value('user_id')
    num_recs = get_param_value('num_recs')

    ctrl = Controller()
    recs = ctrl.get_recs_using_model(user_id, num_recs, algo, None)
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
    user_id = int(get_param_value('user_id'))
    items = get_param_value('items')    
    ctrl = Controller()
    items = list(map(int, items.split(',')))

    # TODO: Add these two parameters to use in the algos
    # use exclusion_list and candidate_list

    recs = ctrl.get_recs_using_model(user_id, None, algo, items)
    return jsonify({'predictions': recs})

@app.route('/algorithms/<algo>/info', methods=['GET'])
def get_model_info(algo):
    ctrl = Controller()
    return jsonify({'model': ctrl.get_model_info(algo)})

@app.route('/algorithms/<algo>/modelfile', methods=['PUT'])
def upload_model(algo):
    ctrl = Controller()
    keys = list(request.files.keys())
    if len(keys) > 0:
        file = request.files.get(keys[0], None)
        ctrl.upload_model(algo, file) # upload the first entry file
        return jsonify({'result': 'ok'})
    else:
        return jsonify({'result': 'No file sent'})

# print('loading models...')
# Controller.preload_models()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')