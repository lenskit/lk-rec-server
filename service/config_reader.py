import json

def get_value(key):
    """
        Get the value for the key sent by using the config.json
    """
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
    return data[key]
