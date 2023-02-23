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
        pass

    # @skip
    @mock.patch.dict(os.environ, env)
    def test_gene_to_acc(self):
        MapGene().gene_to_acc()

    @skip
    @mock.patch.dict(os.environ, env)
    def test_gene_to_refseq(self):
        MapGene().gene_to_refseq()

    @skip
    @mock.patch.dict(os.environ, env)
    def test_gene_to_pubmed(self):
        MapGene().gene_to_pubmed()