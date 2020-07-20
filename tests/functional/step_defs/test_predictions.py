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
    right_url = 'algorithms/popular/info'
    response = requests.get(BASE_URL_API + right_url)
    print(response)
    assert len(response.json()['model']) > 0

@given('the predict API is called with <user_id> and <items>')
def predictions_response(user_id, items):
    params = {'user_id': user_id, 'items': items, 'format': 'json'}
    right_url = 'algorithms/bias/predictions'
    response = requests.get(BASE_URL_API + right_url, params=params)
    return response

# Then Steps
@then('the response returns a list of recommendations')
def get_response_list_recs(recommendations_response):
    recs = recommendations_response.json()['recommendations']
    assert len(recs) > 0
    assert recs[0]['score'] > 0