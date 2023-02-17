'''
Test class 
'''
from unittest import TestCase, mock
from ddt import ddt, data, unpack
import os, sys

from connector.redis import Redis

class Test_(TestCase):

    def setUp(self):
        self.r = Redis()

    def test_get_data(self):
        self.r.update_data('ols', {'id':4})
        res = self.r.get_data('ols')
        assert res['id'] == 4