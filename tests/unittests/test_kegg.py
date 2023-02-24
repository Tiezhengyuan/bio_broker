'''
Test class 
'''
from unittest import TestCase, mock, skip
from ddt import ddt, data, unpack
import os, sys

DIR_CACHE = "H:\\cache"
DIR_DOWNLOAD = "H:\\download"

from database.kegg import KEGG

env = {
    'DIR_CACHE': "H:\\cache",
    'DIR_DOWNLOAD': "H:\\download",
}

@ddt
class TestKEGG(TestCase):

    @mock.patch.dict(os.environ, env)
    def setUp(self):
        self.c = KEGG()


    def test_download_data(self):
        res = self.c.download_data()
        print(res)
