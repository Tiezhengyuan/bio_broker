'''
Test class 
'''
from unittest import TestCase, mock, skip
from ddt import ddt, data, unpack
import os, sys

from database.taxonomy import Taxonomy

env = {
    'DIR_CACHE': "F:\\bio_broker\\cache",
    'DIR_DOWNLOAD': "F:\\bio_broker\\download",
}

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
