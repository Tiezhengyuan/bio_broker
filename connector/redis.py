"""
cache data
"""
import redis
import json

class Redis(object):
    def __init__(self, host=None, port=None, db=None):
        self.host = host if host else 'localhost'
        self.port = port if port else 6379
        self.db = db if db else 0
    
        # default redis database of ontology is 0
        self.conn = redis.StrictRedis(host=self.host,
            port=self.port, db=0)
    
    def get_data(self, key:str):
        data = self.conn.get(key)
        return json.loads(data)

    def update_data(self, key:str, val):
        if isinstance(val, dict):
            val = json.dumps(val)
        self.conn.set(key, val)
