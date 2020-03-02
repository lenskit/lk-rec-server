from flask import Flask, jsonify, abort, make_response, request
from controller import Controller
#from recommender import Recommender

app = Flask(__name__)

@app.route('/lkpy/create_structure', methods=['GET'])
def create_structure():
    ctrl = Controller()
    ctrl.create_db_structure_with_data()
    return jsonify({"result": 'ok'})

# Save all the algo models to disk
# http://127.0.0.1:5001/lkpy/save_models/popular,bias,topn,itemitem,useruser,biasedmf,implicitmf,funksvd
@app.route('/lkpy/save_models/<algos>', methods=['GET'])
def save_models(algos):
    ctrl = Controller()
    ctrl.save_models(algos)
    return jsonify({"result": 'ok'})

@app.route('/lkpy/preloadmodels', methods=['GET'])
def preload_models():
    ctrl = Controller()
    ctrl.preload_models()
    return jsonify({"result": 'ok'})


# Test local urls:
# http://127.0.0.1:5001/lkpy/algorithms/popular/recommendations?user_id=2038&num_recs=10
#@app.route('/lkpy/algorithms/<algo>/recommendations/<int:user_id>/<int:num_recs>', methods=['GET', 'POST'])
@app.route('/lkpy/algorithms/<algo>/recommendations', methods=['GET', 'POST'])
def recommend(algo):
    #if request.method == 'POST':
    user_id = request.args.get('user_id', '')
    num_recs = request.args.get('num_recs', '')

    ctrl = Controller()
    recs = ctrl.get_recs_using_model(user_id, num_recs, algo, None)
    return jsonify({'recommendations': recs})
 
 # Test local urls:
 # http://127.0.0.1:5001/lkpy/predict/bias/22/5,102,203,304,400
 # http://127.0.0.1:5001/lkpy/predict/itemitem/22/100,101,102
 # http://127.0.0.1:5001/lkpy/predict/useruser/22/100,101,102
 # http://127.0.0.1:5001/lkpy/predict/biasedmf/22/100,101,102
 # http://127.0.0.1:5001/lkpy/predict/implicitmf/22/100,101,102
 # http://127.0.0.1:5001/lkpy/predict/funksvd/22/100,101,102
@app.route('/lkpy/algorithms/<algo>/predictions', methods=['GET', 'POST'])
def predict(algo):
    user_id = request.args.get('user_id', '')
    items = request.args.get('items', '')    
    ctrl = Controller()
    items = list(map(int, items.split(',')))
    recs = ctrl.get_recs(user_id, None, algo, items)
    return jsonify({'predictions': recs})

@app.route('/lkpy/algorithms/<algo>/info', methods=['GET'])
def get_model_info(algo):
    ctrl = Controller()
    return jsonify({'model': ctrl.get_model_info(algo)})

@app.route('/lkpy/algorithms/<algo>/modelfile', methods=['POST'])
def upload_model(algo, data):
    ctrl = Controller()
    ctrl.upload_model(algo, data)
    return jsonify({'result': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)