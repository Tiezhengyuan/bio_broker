'''
Test class 
'''
from unittest import TestCase, mock, skip
from ddt import ddt, data, unpack
import os, sys

from annotation.map_protein import MapProtein

env = {
    'DIR_CACHE': "H:\\cache",
    'DIR_DOWNLOAD': "H:\\download",
}

@ddt
class TestMapProtein(TestCase):

    @mock.patch.dict(os.environ, env)
    def setUp(self):
        self.c = MapProtein()

    
    @mock.patch.dict(os.environ, env)
    def test_process(self):
        self.c.process()
