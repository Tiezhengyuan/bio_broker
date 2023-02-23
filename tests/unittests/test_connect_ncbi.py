'''
Test class 
'''
from unittest import TestCase, mock, skip
from ddt import ddt, data, unpack
import os, sys

DIR_CACHE = "F:\\bio_broker\\cache"
DIR_DOWNLOAD = "F:\\bio_broker\\download"

from connector.connect_ncbi import ConnectNCBI

@ddt
class TestConnectNCBI(TestCase):

    def setUp(self):
        self.endpoint = 'ftp.ncbi.nlm.nih.gov'

    @mock.patch.dict(os.environ, {'DIR_DOWNLOAD': DIR_DOWNLOAD})
    def test_download_gene_data(self):
        res = ConnectNCBI().download_gene_data()
        print(res)
