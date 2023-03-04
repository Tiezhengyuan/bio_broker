'''
Test class 
'''
from tests.helper import *

from database.kegg import KEGG


@ddt
class TestKEGG(TestCase):

    @mock.patch.dict(os.environ, env)
    def setUp(self):
        self.c = KEGG()


    def test_download_data(self):
        res = self.c.download_data()
        print(res)
