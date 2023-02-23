'''
Test class 
'''
from unittest import TestCase, mock
from ddt import ddt, data, unpack
import os, sys

from annotation.map_gene import MapGene

env = {
    'DIR_CACHE': "F:\\bio_broker\\cache",
    'DIR_DOWNLOAD': "F:\\bio_broker\\download",
}

@ddt
class TestMapGene(TestCase):

    def setUp(self):
        pass

    @mock.patch.dict(os.environ, env)
    def test_(self):
        MapGene().gene_to_acc()