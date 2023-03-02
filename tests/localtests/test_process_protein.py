'''
Test class 
'''
from unittest import TestCase, mock, skip
from ddt import ddt, data, unpack
import os
import pandas as pd
from database.process_protein import ProcessProtein

env = {
    'DIR_CACHE': "H:\\cache",
    'DIR_DOWNLOAD': "H:\\download",
}


@ddt
class TestProcessProtein(TestCase):
    
    @mock.patch.dict(os.environ, env)
    def setUp(self):
        self.c = ProcessProtein(debugging=True)

    @mock.patch.dict(os.environ, env)
    def test_parse_ncbi_protein(self):
        self.c.parse_ncbi_protein()
