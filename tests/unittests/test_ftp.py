'''
Test class 
'''
from unittest import TestCase, mock, skip
from ddt import ddt, data, unpack
import os, sys

DIR_CACHE = "F:\\bio_broker\\cache"
DIR_DOWNLOAD = "F:\\bio_broker\\download"

from connector.connect_ftp import ConnectFTP

@ddt
class Test_(TestCase):

    def setUp(self):
        self.endpoint = 'ftp.ncbi.nlm.nih.gov'

    @skip
    @data(
        ['geo/series/GSE3nnn/GSE3341/matrix', True],
        ['geo/series/GSE3nnn/GSE3341/matrix/GSE3341_series_matrix.txt.gz', False],
        ['', True],
    )
    @unpack
    @mock.patch.dict(os.environ, {'DIR_DOWNLOAD': DIR_DOWNLOAD})
    def test_is_dir(self, path, expect):
        res = ConnectFTP(self.endpoint).is_dir(path)
        assert res == expect


    @skip
    @data(
        ['geo/series/GSE3nnn/GSE3341/matrix', '.gz', 1],
        ['geo/series/GSE3nnn/GSE3341/', '.gz', 0],
        ['geo/series/GSE3nnn/GSE3341/', None, 0],
    )
    @unpack
    @mock.patch.dict(os.environ, {'DIR_DOWNLOAD': DIR_DOWNLOAD})
    def test_download_files(self, path, pattern, expect):
        res = ConnectFTP(self.endpoint).download_files(path, pattern)
        assert len(res) == expect


    @data(
        ['GSE3341', 'geo/series/GSE3nnn/GSE3341/', None, 3],
    )
    @unpack
    @mock.patch.dict(os.environ, {'DIR_DOWNLOAD': DIR_DOWNLOAD})
    def test_download_tree(self, local_name, path, pattern, expect):
        res = ConnectFTP(self.endpoint).download_tree(
            local_name, path, pattern)
        assert len(res) == expect
