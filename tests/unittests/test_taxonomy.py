'''
Test class 
'''
from tests.helper import *
from database.taxonomy import Taxonomy


@ddt
class TestTaxonomy(TestCase):

    def setUp(self):
        pass

    @skip
    @mock.patch.dict(os.environ, env)
    def test_download_taxonomy(self):
        res = Taxonomy().download_taxonomy()
        assert res == True

    @skip
    @mock.patch.dict(os.environ, env)
    def test_get_taxonomy(self):
        Taxonomy().get_taxonomy()

    @data(
        [24, 'Shewanella putrefaciens'],
        [9606, 'Homo sapiens']
    )
    @unpack
    @mock.patch.dict(os.environ, env)
    def test_search_by_tax_id(self, tax_id, expect):
        res = Taxonomy().search_by_tax_id(tax_id)
        assert res['ScientificName'] == expect
