'''
Test class 
'''
from tests.helper import *

from database.geo import GEO


@ddt
class Test_(TestCase):

    def setUp(self):
        pass


    # @skip
    @data(
        # ["GSE16[acc]", 27],
        # ["GSE152641[acc]", None],
        ["covid-19[title]", 27],
    )
    @unpack
    def test_retrieve_uids(self, GSE, samples):
        res = GEO().retrieve_uids(GSE)
        print(res, len(res))

    @skip 
    @data(
        # [['200000016',],],
        [['100000028', '200000016','300000794','300000795',],],
    )
    @unpack
    def test_retrieve_summary(self, id_list):
        res = GEO().retrieve_summary(id_list)
        print(res)

    @skip
    @data(
       ["GSE152641",],
    )
    @unpack
    @mock.patch.dict(os.environ, env)
    def test_download_data(self, GSE):
        res = GEO().download_data(GSE)

    @skip
    @data(
       ["GSE152641",],
    )
    @unpack
    @mock.patch.dict(os.environ, env)
    def test_read_data(self, GSE):
        metadata, data, counts = GEO().read_data(GSE)
