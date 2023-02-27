'''
Test class 
'''
from unittest import TestCase, mock, skip
from ddt import ddt, data, unpack
import os

from annotation.map import Map

env = {
    'DIR_CACHE': "H:\\cache",
    'DIR_DOWNLOAD': "H:\\download",
}


@ddt
class TestMap(TestCase):

    @mock.patch.dict(os.environ, env)
    def setUp(self):
        self.c = Map()


    @data(
        ['9606', "2", "NP_001334352.2"],
    )
    @unpack
    def test_geneid_to_protein_accession(self, tax_id, expect_uid, expect):
        map, rev_map = self.c.get_map(
            f"{tax_id}_gene2refseq.jtxt",
            "protein_accession.version",
            lambda x: list(set(x))
        )
        assert expect_uid in map
        assert expect in rev_map


    @skip
    @data(
        ['9606', "100008586", "GAGE12F"],
    )
    @unpack
    def test_geneid_to_symbol(self, tax_id, expect_uid, expect_symbol):
        map, rev_map = self.c.get_map(
            f"{tax_id}_gene2accession.jtxt",
            'Symbol'
        )
        assert expect_uid in map
        assert expect_symbol in rev_map


    @skip
    @data(
        ['9606', "100008586", ["X"]],
        ['9606', "wrong_id", None],
    )
    @unpack
    def test_geneid_to_chromosome(self, tax_id, uid, expect):
        map, _ = self.c.get_map(
            f"{tax_id}_gene_info.jtxt",
            'chromosome'
        )
        assert map.get(uid) == expect

    @skip
    @data(
        ['9606', "100008586", ["32413"]],
        ['9606', "wrong_id", None],
    )
    @unpack
    def test_geneid_to_start(self, tax_id, uid, expect):
        map, _ = self.c.get_map(
            f"{tax_id}_gene2accession.jtxt",
            'start_position_on_the_genomic_accession'
        )
        assert map.get(uid) == expect
    
    @skip
    @data(
        ['9606', 'ENSG00000236362', ["100008586"],],
        ['9606', "wrong_id", None,],
    )
    @unpack
    def test_ensembl_geneacc_to_geneid(self, tax_id, acc, expect):
        map = self.c.get_intra_map(
            f"{tax_id}_gene2ensembl.jtxt",
            "Ensembl_gene_identifier",
            "GeneID"
        )
        assert map.get(acc) == expect

    @skip
    @data(
        ['9606', "ENSP00000404123.1", ["100008586"],],
        ['9606', "wrong_id", None,],
    )
    @unpack
    def test_ensembl_proacc_to_geneid(self, tax_id, acc, expect):
        map = self.c.get_intra_map(
            f"{tax_id}_gene2ensembl.jtxt",
            "Ensembl_protein_identifier",
            "GeneID"
        )
        assert map.get(acc) == expect

    @skip
    @data(
        ['9606', "ENST00000440137.2", ["100008586"],],
        ['9606', "wrong_id", None,],
    )
    @unpack
    def test_ensembl_rnaacc_to_geneid(self, tax_id, acc, expect):
        map = self.c.get_intra_map(
            f"{tax_id}_gene2ensembl.jtxt",
            "Ensembl_rna_identifier",
            "GeneID"
        )
        assert map.get(acc) == expect

