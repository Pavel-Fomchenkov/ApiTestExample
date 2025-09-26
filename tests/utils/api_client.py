import requests


class ApiClient:

    def __init__(self, base_url):
        self.base_url = base_url

    def post(self, endpoint, data=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, json=data, headers=headers)
        return response

    def get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, params)
        return response

    def put(self, endpoint, data=None, headers=None, cookies=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.put(url, json=data, headers=headers, cookies=cookies)
        return response

    def patch(self, endpoint, data=None, headers=None, cookies=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.patch(url, json=data, headers=headers, cookies=cookies)
        return response

    def delete(self, endpoint, headers=None, cookies=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.delete(url, headers=headers, cookies=cookies)
        return response