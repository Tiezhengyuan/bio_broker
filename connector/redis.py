"""
cache data
"""
import redis

class Redis(object):
    def __init__(self, host, port):
        self.host = host else 'localhost'
        self.port = port else 6379
        self.c = redis.Redis((host, port))