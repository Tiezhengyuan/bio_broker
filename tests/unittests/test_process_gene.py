'''
Test class 
'''
from unittest import TestCase, mock, skip
from ddt import ddt, data, unpack
import os

from database.process_gene import ProcessGene

env = {
    'DIR_CACHE': "H:\\cache",
    'DIR_DOWNLOAD': "H:\\download",
}


@ddt
class TestProcessGene(TestCase):
    
    @mock.patch.dict(os.environ, env)
    def setUp(self):
        self.c = ProcessGene()

    @mock.patch.dict(os.environ, env)
    def test_process(self):
        self.c.process_map('9606')


    @skip
    @mock.patch.dict(os.environ, env)
    def test_gene_to_accession(self):
        self.c.gene_to_accession('9606')

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
    def test_parse_orthologs(self):
        self.c.parse_orthologs('9606')

    @skip
    def test_parse_neighbors(self):
        self.c.parse_neighbors('9606')


    @skip
    def test_parse_history(self):
        self.c.parse_history('9606')

    @skip
    def test_parse_group(self):
        self.c.parse_group('9606')

    @skip
    def test_parse_info(self):
        self.c.parse_info('9606')
