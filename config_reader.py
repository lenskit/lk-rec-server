import json

class ConfigReader:

    def read_config(self, key):
        with open('config.json') as json_data_file:
            data = json.load(json_data_file)
        print(data)
        print(data[key])
        return data
