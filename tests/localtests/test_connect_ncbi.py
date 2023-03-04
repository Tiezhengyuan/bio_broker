'''
Test class ConnectNCBI
'''
from tests.helper import *

from connector.connect_ncbi import ConnectNCBI

@ddt
class TestConnectNCBI(TestCase):

    def setUp(self):
        self.endpoint = 'ftp.ncbi.nlm.nih.gov'

    @skip
    @mock.patch.dict(os.environ, {'DIR_DOWNLOAD': os.getenv('DIR_DOWNLOAD')})
    def test_download_gene_data(self):
        res = ConnectNCBI().download_gene_data()
        print(res)

    def test_(self):
        print(os.getenv('DIR_DOWNLOAD'))