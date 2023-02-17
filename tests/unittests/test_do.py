'''
Test class 
'''
from unittest import TestCase, mock
from ddt import ddt, data, unpack
import os, sys

from ontology.do import DiseaseOntology

class Test_(TestCase):

    def setUp(self):
        self.c = DiseaseOntology()

    def test_get_doid(self):
        res = self.c.get_doid()
        term = res.get('DOID:0001816')
        assert term['name'] == 'angiosarcoma'
        