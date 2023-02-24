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

    @mock.patch.dict(os.environ, env)
    def setUp(self):
        self.c = MapGene()


    @skip
    @data(
        ['9606', "100008586", "GAGE12F"],
    )
    @unpack
    def test_geneid_to_symbol(self, tax_id, expect_uid, expect_symbol):
        map, rev_map = self.c.geneid_to_symbol(tax_id)
        assert expect_uid in map
        assert expect_symbol in rev_map


    @skip
    @data(
        ['9606', "100008586", ["X"]],
        ['9606', "wrong_id", None],
    )
    @unpack
    def test_geneid_to_chromosome(self, tax_id, uid, expect):
        map, _ = self.c.geneid_to_chromosome(tax_id)
        assert map.get(uid) == expect

    @skip
    @data(
        ['9606', "100008586", ["32413"]],
        ['9606', "wrong_id", None],
    )
    @unpack
    def test_geneid_to_start(self, tax_id, uid, expect):
        map, _ = self.c.geneid_to_start_position(tax_id)
        assert map.get(uid) == expect
    
    @skip
    @data(
        ['9606', 'ENSG00000236362', ["100008586"],],
        ['9606', "wrong_id", None,],
    )
    @unpack
    def test_ensembl_geneacc_to_geneid(self, tax_id, acc, expect):
        map = self.c.ensembl_geneacc_to_geneid(tax_id)
        assert map.get(acc) == expect

    @skip
    @data(
        ['9606', "ENSP00000404123.1", ["100008586"],],
        ['9606', "wrong_id", None,],
    )
    @unpack
    def test_ensembl_proacc_to_geneid(self, tax_id, acc, expect):
        map = self.c.ensembl_proacc_to_geneid(tax_id)
        assert map.get(acc) == expect

    @skip
    @data(
        ['9606', "ENST00000440137.2", ["100008586"],],
        ['9606', "wrong_id", None,],
    )
    @unpack
    def test_ensembl_rnaacc_to_geneid(self, tax_id, acc, expect):
        map = self.c.ensembl_rnaacc_to_geneid(tax_id)
        assert map.get(acc) == expect
