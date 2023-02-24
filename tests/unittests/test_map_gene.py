'''
Test class 
'''
from unittest import TestCase, mock, skip
from ddt import ddt, data, unpack
import os

from annotation.map_gene import MapGene

env = {
    'DIR_CACHE': "H:\\cache",
    'DIR_DOWNLOAD': "H:\\download",
}


@ddt
class TestMapGene(TestCase):

    def setUp(self):
        self.c = MapGene()


    @skip
    @data(
        ['9606', "100008586", "GAGE12F"],
    )
    @unpack
    @mock.patch.dict(os.environ, env)
    def test_geneid_to_symbol(self, tax_id, expect_uid, expect_symbol):
        map, rev_map = self.c.geneid_to_symbol(tax_id)
        assert expect_uid in map
        assert expect_symbol in rev_map