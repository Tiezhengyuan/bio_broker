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
        ['9606',],
    )
    @unpack
    @mock.patch.dict(os.environ, env)
    def test_process_taxonomy_map(self, tax_id):
        self.c.process_taxonomy_map(tax_id)


    @skip
    @data(
        ['9606',],
    )
    @unpack
    @mock.patch.dict(os.environ, env)
    def test_map_gene_to_uniprotkb(self, tax_id):
        self.c.map_gene_to_uniprotkb(tax_id)
