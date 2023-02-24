'''
Test class 
'''
from unittest import TestCase, mock, skip
from ddt import ddt, data, unpack
import os

from annotation.process_gene import ProcessGene

env = {
    'DIR_CACHE': "H:\\cache",
    'DIR_DOWNLOAD': "H:\\download",
}


@ddt
class TestProcessGene(TestCase):

    def setUp(self):
        self.c = ProcessGene()

    @skip
    @mock.patch.dict(os.environ, env)
    def test_gene_to_accession(self):
        self.c.gene_to_accession()

    @skip
    @mock.patch.dict(os.environ, env)
    def test_gene_to_refseq(self):
        self.c.gene_to_refseq()

    @skip
    @mock.patch.dict(os.environ, env)
    def test_gene_to_pubmed(self):
        self.c.gene_to_pubmed('9606')

    @skip
    @mock.patch.dict(os.environ, env)
    def test_gene_to_go(self):
        self.c.gene_to_go('9606')

    @skip
    @mock.patch.dict(os.environ, env)
    def test_gene_to_ensembl(self):
        self.c.gene_to_ensembl('9606')


    @skip
    @mock.patch.dict(os.environ, env)
    def test_parse_uniprotkb(self):
        self.c.parse_uniprotkb('9606')

    @skip
    @mock.patch.dict(os.environ, env)
    def test_parse_orthologs(self):
        self.c.parse_orthologs('9606')

    # @skip
    @mock.patch.dict(os.environ, env)
    def test_parse_neighbors(self):
        self.c.parse_neighbors('9606')


