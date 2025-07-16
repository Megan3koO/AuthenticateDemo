import requests
import json

class RequestsMaker:
    def __init__(self, base_url='http://localhost:3000'):
        self.base_url = base_url

    def send_get_request(self, endpoint, params=None, headers=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.status_code, response.json()
        else:
            return response.status_code, {"error_message" : response.text}
        
    def send_post_request_json(self, endpoint, json=None, headers=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, json=json)
        if response.status_code == 201:
            return response.status_code, response.json()
        else:
            return response.status_code, {"error_message" : response.text}