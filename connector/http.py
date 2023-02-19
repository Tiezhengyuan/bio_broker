
import requests
import json
import os

class HTTP:
    def __init__(self, endpoint:str):
        self.endpoint = endpoint
    
    def retrieve_data(self, path=None, parameters=None):
        url = f"{self.endpoint}{path}" if path else self.endpoint
        # print(url)
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
    
    def download_file(self, outdir, path=None):
        '''
        Download file from HTTP web 
        '''
        url = f"{self.endpoint}{path}" if path else self.endpoint
        outfile = os.path.join(outdir, os.path.basename(path))
        try:
            with open(outfile, 'wb') as f:
                res = requests.get(url)
                f.write(res.content)
            return outfile
        except Exception as e:
            print(e)
        return False