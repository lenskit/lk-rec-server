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
        timeout=30.0, pause=0.1, check=lambda: is_responsive(url)
    )
    return url

# Scenarios
scenarios('../features/models.feature', example_converters=dict(user_id=int, num_recs=int))

# Given Steps
@given('a running recommendation server')
def is_server_running(http_service):
    response = requests.get(http_service + "status")
    print(response)
    print(response.json())
    assert response.status_code == 200

@given('a trained recommender model for <algo>')
def get_trained_model_response(http_service, algo):
    right_url = f'algorithms/{algo}/info'
    response = requests.get(http_service + right_url)
    # assert len(response.json()['model']) > 0
    return response

@given('upload model for <algo>')
def get_upload_model_response(algo, http_service):
    right_url = f'algorithms/{algo}/modelfile'
    model_name = algo + ".bpk"
    file_path = "tests/functional/test_files/" + model_name
    files = {
        'file': open(file_path, 'rb')
    }
    response = requests.put(http_service + right_url, files=files)
    return response


@then('the response returns the model creation_date and size')
def get_model_creation_date_and_size(get_trained_model_response):
    model = get_trained_model_response.json()['model']
    assert model['creation_date'] != None
    assert model['size'] != 0

@then('the response returns empty information for the model')
def get_model_empty_information(get_trained_model_response):
    model = get_trained_model_response.json()['model']
    assert model == {}    

@then(parsers.parse('the response status code is "{code:d}"'))
def ddg_response_code(get_trained_model_response, code):
    assert get_trained_model_response.status_code == code

@then(parsers.parse('the response status code is "{code:d}" and "{result}"'))
def ddg_upload_model_response_code(get_upload_model_response, code, result):
    print(get_upload_model_response)
    print(get_upload_model_response.json())
    assert get_upload_model_response.status_code == code
    assert get_upload_model_response.json()['result'] == result