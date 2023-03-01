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

    # @skip
    @mock.patch.dict(os.environ, env)
    def test_process_taxonomy_entrez(self):
        self.c.process_taxonomy_entrez('9606')

    @skip
    @mock.patch.dict(os.environ, env)
    def test_parse_taxonomy_gene2(self):
        handle = self.c.parse_taxonomy_gene2('gene2accession', '9606')
        res = next(handle)
        assert '1' in res


    # @skip
    # @mock.patch.dict(os.environ, env)
    # def test_parse_uniprotkb(self):
    #     outfile = ''
    #     self.c.parse_uniprotkb(outfile)

