'''
Test class 
'''
from unittest import TestCase, mock, skip
from ddt import ddt, data, unpack
import os, sys

from database.expasy import ExPASy

env = {
    'DIR_CACHE': "H:\\cache",
    'DIR_DOWNLOAD': "H:\\download",
}

@ddt
class TestKEGG(TestCase):

    @mock.patch.dict(os.environ, env)
    def setUp(self):
        self.c = ExPASy()

    @skip
    def test_parse_enzyme(self):
        self.c.parse_enzyme()

    @skip
    @data(
        ["1.1.1.1", 'alcohol dehydrogenase'],
        ["EC1.1.1.1", 'alcohol dehydrogenase'],
        ["EC 1.1.1.1", 'alcohol dehydrogenase'],
        ['wrong_id', None]
    )
    @unpack
    def test_gene_enzyme_annotation(self, ec, name):
        res = self.c.gene_enzyme_annotation(ec)
        assert res.get('name') == name

    @skip
    @data(
        ["P07327",  ["1.1.1.1"], ],
        ['Q9RR46', ['7.6.2.9'], ],
        ['wrong_id', None]
    )
    @unpack
    def test_uniprotkb_to_ec(self, swissprot_id, ec):
        res = self.c.uniprotkb_to_ec()
        assert res.get(swissprot_id) == ec

    @data(
        ['alcohol dehydrogenase', False, 17],
        ['dehydrogenase', True, 613],
        ['wrong_term', True, 0]
    )
    @unpack
    def test_search_enzymes(self, term, cc, expect):
        res = self.c.search_enzymes(term, cc)
        assert len(list(res)) >= expect
