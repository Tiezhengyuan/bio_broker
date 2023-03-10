'''
Test class 
'''
from tests.helper import *
from ontology.go import GeneOntology

class Test_(TestCase):

    def setUp(self):
        self.c = GeneOntology()

    def test_get_bioentity(self):
        res = self.c.get_bioentity('GO:0006915')
        assert res.get('label') == "apoptotic process"