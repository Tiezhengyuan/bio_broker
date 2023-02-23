'''
Test class 
'''
from unittest import TestCase, mock, skip
from ddt import ddt, data, unpack
import os, sys

DIR_CACHE = "F:\\bio_broker\\cache"
DIR_DOWNLOAD = "F:\\bio_broker\\download"

from utils.dir import Dir

@ddt
class TestDir(TestCase):

    def setUp(self):
        self.endpoint = 'ftp.ncbi.nlm.nih.gov'

    # @skip
    @data(
        ['a', True],
        [os.path.join('a', 'b', 'c'), True],
    )
    @unpack
    def test_init_dir(self, path, expect):
        indir = os.path.join(DIR_DOWNLOAD, path)
        res = Dir(indir).init_dir()
        assert res == expect