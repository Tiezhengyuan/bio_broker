
import requests

class HTTP:
    def __init__(self, endpoint:str, route:str):
        self.url = f"{endpoint}{route}"
    
    def retrieve_data(self, parameters=None:dict):
        if parameters:
            par = '&'.join([ f"{k}={v}" for k,v in parameters.items()])
            self.url += f"?{par}"

        res = requests.get(self.url)
        if res.status_code == 200:
            return res.text
        return res.status_code