'''
Test class 
'''
from datetime import datetime
from unittest import TestCase, mock, skip
from ddt import ddt, data, unpack
import os, sys

DIR_BIN = "F:\\bio_broker\\bin"
DIR_CACHE = "F:\\bio_broker\\cache"
DIR_DOWNLOAD = "F:\\bio_broker\\download"


from database.genbank import GenBank


@ddt
class Test_(TestCase):

    def setUp(self):
        pass

    @skip
    @data(
        # return GI 
        ["Cypripedioideae[Orgn] AND matK[Gene]", None],
        # return accession number
        ["Homo sapiens[Orgn] AND Covid-19[title]", 'acc']
    )
    @unpack
    def test_search_genbank(self, term, idtype):
        res = GenBank().search_genbank(term, idtype=idtype)
        for i in res:
            print(i)

    @data(
        # [['PA544334.1',], None, None],
        [['808037376', '808037374',], 'fasta', 'xml'],
    )
    @unpack
    def test_retrieve_records(self, id_list, rettype, retmode):
        res = GenBank().retrieve_records(id_list, \
            rettype=rettype, retmode=retmode)
        print(res)
