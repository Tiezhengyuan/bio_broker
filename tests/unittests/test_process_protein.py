'''
Test class 
'''
from unittest import TestCase, mock, skip
from ddt import ddt, data, unpack
import os

from database.process_protein import ProcessProtein

env = {
    'DIR_CACHE': "H:\\cache",
    'DIR_DOWNLOAD': "H:\\download",
}


@ddt
class TestProcessProtein(TestCase):
    
    @mock.patch.dict(os.environ, env)
    def setUp(self):
        self.c = ProcessProtein()

    # @skip
    @mock.patch.dict(os.environ, env)
    def test_process_protein(self):
        self.c.process_protein()
