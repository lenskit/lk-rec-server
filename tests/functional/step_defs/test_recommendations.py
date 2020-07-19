import requests

from pytest_bdd import scenarios, given, then, parsers

BASE_URL_API = 'http://127.0.0.1:5000/'

# Scenarios
scenarios('../features/recommendations.feature', example_converters=dict(user_id=int, num_recs=int))

# Given Steps
@given('a running recommendation server')
def is_server_running():
    response = requests.get(BASE_URL_API)
    assert response.status_code == 404

@given('a trained ALS recommender model')
def get_trained_als_model():
    right_url = 'algorithms/popular/info'
    response = requests.get(BASE_URL_API + right_url)
    print(response)
    assert len(response.json()['model']) > 0

@given('the recommend API is called with <user_id> and <num_recs>')
def recommendations_response(user_id, num_recs):
    params = {'user_id': user_id, 'num_recs': num_recs, 'format': 'json'}
    right_url = 'algorithms/popular/recommendations'
    response = requests.get(BASE_URL_API + right_url, params=params)
    return response

@given('Given the default recommendation endpoint is called with <user_id> and <num_recs>')
def recommendations_response(user_id, num_recs):
    params = {'user_id': user_id, 'num_recs': num_recs, 'format': 'json'}
    right_url = 'recommendations'
    response = requests.get(BASE_URL_API + right_url, params=params)
    return response

# Then Steps
@then('the response returns a list of recommendations')
def get_response_list_recs(recommendations_response):
    recs = recommendations_response.json()['recommendations']
    assert len(recs) > 0
    assert recs[0]['score'] > 0

@then('the response has <num_recs> items')
def get_response_num_items(recommendations_response, num_recs):
    assert len(recommendations_response.json()['recommendations']) == num_recs


@then(parsers.parse('the response status code is "{code:d}"'))
def ddg_response_code(recommendations_response, code):
    assert recommendations_response.status_code == code

