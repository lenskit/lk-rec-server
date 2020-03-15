from flask import Flask, jsonify, abort, make_response, request
from controller import Controller
from config_reader import ConfigReader

app = Flask(__name__)

@app.route('/create_structure', methods=['GET'])
def create_structure():
    ctrl = Controller()
    ctrl.create_db_structure_with_data()
    return jsonify({"result": 'ok'})

# Save all the algo models to disk
# http://127.0.0.1:5001/save_models/popular,bias,topn,itemitem,useruser,biasedmf,implicitmf,funksvd
@app.route('/save_models/<algos>', methods=['GET'])
def save_models(algos):
    ctrl = Controller()
    ctrl.save_models(algos)
    return jsonify({"result": 'ok'})

@app.route('/preloadmodels', methods=['GET'])
def preload_models():
    ctrl = Controller()
    ctrl.preload_models()
    return jsonify({"result": 'ok'})


# Default algo path:
# 	/recommendations
@app.route('/recommendations', methods=['GET', 'POST'])
def recommend_default():
    reader = ConfigReader()
    algo = reader.get_value("default_algorithm")
    return recommend(algo)


# Test local urls:
# http://127.0.0.1:5001/algorithms/popular/recommendations?user_id=2038&num_recs=10
#@app.route('/algorithms/<algo>/recommendations/<int:user_id>/<int:num_recs>', methods=['GET', 'POST'])
@app.route('/algorithms/<algo>/recommendations', methods=['GET', 'POST'])
def recommend(algo):
    #if request.method == 'POST':
    user_id = request.args.get('user_id', '')
    num_recs = request.args.get('num_recs', '')

    ctrl = Controller()
    recs = ctrl.get_recs_using_model(user_id, num_recs, algo, None)
    return jsonify({'recommendations': recs})
 
 # Test local urls:
 # http://127.0.0.1:5001/algorithms/bias/predictions/22/5,102,203,304,400
 # http://127.0.0.1:5001/algorithms/itemitem/predictions/22/100,101,102
 # http://127.0.0.1:5001/algorithms/useruser/predictions/22/100,101,102
 # http://127.0.0.1:5001/algorithms/biasedmf/predictions/22/100,101,102
 # http://127.0.0.1:5001/algorithms/implicitmf/predictions/22/100,101,102
 # http://127.0.0.1:5001/algorithms/funksvd/predictions/22/100,101,102
@app.route('/algorithms/<algo>/predictions', methods=['GET', 'POST'])
def predict(algo):
    user_id = request.args.get('user_id', '')
    items = request.args.get('items', '')    
    ctrl = Controller()
    items = list(map(int, items.split(',')))
    recs = ctrl.get_recs(user_id, None, algo, items)
    return jsonify({'predictions': recs})

@app.route('/algorithms/<algo>/info', methods=['GET'])
def get_model_info(algo):
    ctrl = Controller()
    return jsonify({'model': ctrl.get_model_info(algo)})

@app.route('/algorithms/<algo>/modelfile', methods=['POST'])
def upload_model(algo, data):
    ctrl = Controller()
    ctrl.upload_model(algo, data)
    return jsonify({'result': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)