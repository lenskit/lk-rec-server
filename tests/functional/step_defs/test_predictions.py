import pytest
import requests

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
        timeout=60.0, pause=0.1, check=lambda: is_responsive(url)
    )
    return url

# Scenarios
scenarios('../features/predictions.feature', example_converters=dict(user_id=int, num_recs=int))

# Given Steps
@given('a running recommendation server')
def is_server_running(http_service):
    response = requests.get(http_service + "status")    
    assert response.status_code == 200

@given('a trained recommender model')
def get_trained_als_model(http_service):
    right_url = 'algorithms/biasedmf/info'
    response = requests.get(http_service + right_url)
    assert len(response.json()['model']) > 0

@given('the predict API is called with <user_id> and <items>')
def predictions_response(http_service, user_id, items):
    params = {'user_id': user_id, 'items': items, 'format': 'json'}
    right_url = 'algorithms/biasedmf/predictions'
    response = requests.get(http_service + right_url, params=params)
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
    print(predictions_response.text)
    assert predictions_response.status_code == code