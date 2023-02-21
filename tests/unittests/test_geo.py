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


from database.geo import GEO


@ddt
class Test_(TestCase):

    def setUp(self):
        pass


    @skip
    @data(
        ["GSE16", None],
    )
    @unpack
    def test_search_geo(self, term, idtype):
        res = GEO().search_geo(term, idtype=idtype)
        for i in res:
            print(i)

    @skip
    @data(
        [['200000016',],],
        [['100000028', ],],
        [['200003341',],]
    )
    @unpack
    def test_retrieve_records(self, id_list):
        res = GEO().retrieve_records(id_list)
