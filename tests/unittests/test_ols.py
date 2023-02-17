
'''
Test class 
'''
from unittest import TestCase, mock
from ddt import ddt, data, unpack
import os, sys

from ontology.ols import OntologyLookupService

class Test_(TestCase):

    def setUp(self):
        self.c = OntologyLookupService()

    def test_get_ontology_list(self):
        res = self.c.get_ontology_list()
        ontology = res.get('sbo', {})
        assert ontology.get('ontologyId') == "sbo"