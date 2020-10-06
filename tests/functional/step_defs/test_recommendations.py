import pytest
import requests
import logging

from pytest_bdd import scenarios, given, then, parsers
from requests.exceptions import ConnectionError

def is_responsive(url):
    try:
        response = requests.get(url)
        if response.status_code == 404:
            return True
    except ConnectionError:
        return False    

@pytest.fixture(scope="session")
def http_service(docker_ip, docker_services):
    """Ensure that HTTP service is up and responsive."""

    # `port_for` takes a container port and returns the corresponding host port
    port = docker_services.port_for("recserver", 5000)
    url = "http://{}:{}/".format(docker_ip, port)
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive(url)
    )
    return url

# Scenarios
scenarios('../features/recommendations.feature', example_converters=dict(user_id=int, num_recs=int))

# Given Steps
@given('a running recommendation server')
def is_server_running(http_service):
    response = requests.get(http_service + "status")
    assert response.status_code == 200

@given('a trained recommender model')
def get_trained_als_model(http_service):
    right_url = 'algorithms/popular/info'
    response = requests.get(http_service + right_url)
    assert len(response.json()['model']) > 0

@given('the recommend API is called with <user_id> and <num_recs>')
def recommendations_response(user_id, num_recs, http_service):
    params = {'user_id': user_id, 'num_recs': num_recs, 'format': 'json'}
    rec_url = 'algorithms/popular/recommendations'
    response = requests.get(http_service + rec_url, params=params)
    return response

@given('the default recommendation endpoint is called with <user_id> and <num_recs>')
def default_recommendations_response(user_id, num_recs, http_service):
    params = {'user_id': user_id, 'num_recs': num_recs, 'format': 'json'}
    right_url = 'recommendations'
    response = requests.get(http_service + right_url, params=params)
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
    if recommendations_response.status_code != code:
        logging.error(recommendations_response.text)
    assert recommendations_response.status_code == code