
import requests
import json


class HTTP:
    def __init__(self, endpoint:str):
        self.endpoint = endpoint
    
    def retrieve_data(self, path=None, parameters=None):
        url = f"{self.endpoint}{path}" if path else self.endpoint
        if parameters:
            par = '&'.join([ f"{k}={v}" for k,v in parameters.items()])
            url += f"?{par}"

        res = requests.get(url)
        if res.status_code == 200:
            return res.text
        return None
    
    def retrieve_json(self, path=None, parameters=None):
        res = self.retrieve_data(path, parameters)
        try:
            return json.loads(res)
        except Exception as e:
            pass
        return {}