import requests

from pytest_bdd import scenarios, given, then, parsers

BASE_URL_API = 'http://127.0.0.1:5000/'

# Scenarios
scenarios('../features/recommendations.feature', example_converters=dict(user_id=int, num_recs=int))

# Given Steps
@given('the recommend API is called with <user_id> and <num_recs>')
def recommendations_response(user_id, num_recs):
    params = {'user_id': user_id, 'num_recs': num_recs, 'format': 'json'}
    right_url = 'algorithms/popular/recommendations'
    response = requests.get(BASE_URL_API + right_url, params=params)
    return response


# Then Steps
@then('the response returns a result list for <user_id> and <num_recs>')
def ddg_response_contents(recommendations_response, user_id, num_recs):
    print(recommendations_response.json()['recommendations'])
    assert len(recommendations_response.json()['recommendations']) == num_recs

@then(parsers.parse('the response status code is "{code:d}"'))
def ddg_response_code(recommendations_response, code):
    assert recommendations_response.status_code == code
