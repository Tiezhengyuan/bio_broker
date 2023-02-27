'''
Test class 
'''
from unittest import TestCase, mock, skip
from ddt import ddt, data, unpack
import os, sys

from database.swissprot import Swissprot

env = {
    'DIR_CACHE': "H:\\cache",
    'DIR_DOWNLOAD': "H:\\download",
}

@ddt
class TestSwissProt(TestCase):

    @mock.patch.dict(os.environ, env)
    def setUp(self):
        self.c = Swissprot()

    @skip
    def test_parse_protein(self):
        handle = self.c.parse_protein()
        res = next(handle)
        assert 'accessions' in res


