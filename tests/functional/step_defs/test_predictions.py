import requests

from pytest_bdd import scenarios, given, then, parsers

BASE_URL_API = 'http://127.0.0.1:5000/'

# Scenarios
scenarios('../features/predictions.feature', example_converters=dict(user_id=int, num_recs=int))

# Given Steps
@given('a running recommendation server')
def is_server_running():
    response = requests.get(BASE_URL_API)
    assert response.status_code == 404

@given('a trained recommender model')
def get_trained_als_model():
    right_url = 'algorithms/biasedmf/info'
    response = requests.get(BASE_URL_API + right_url)
    print(response)
    assert len(response.json()['model']) > 0

@given('the predict API is called with <user_id> and <items>')
def predictions_response(user_id, items):
    params = {'user_id': user_id, 'items': items, 'format': 'json'}
    right_url = 'algorithms/biasedmf/predictions'
    response = requests.get(BASE_URL_API + right_url, params=params)
    return response

# Then Steps
@then('the response returns a list of predictions')
def get_response_list_recs(predictions_response):
    recs = predictions_response.json()['predictions']
    assert len(recs) > 0
    assert recs[0]['score'] > 0

@then('the response returns an empty list')
def get_response_empty_list_recs(predictions_response):
    recs = predictions_response.json()['predictions']
    assert len(recs) == 0

@then(parsers.parse('the response status code is "{code:d}"'))
def ddg_response_code(predictions_response, code):
    assert predictions_response.status_code == code    