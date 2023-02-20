'''
Test class 
'''
from datetime import datetime
from unittest import TestCase, mock
from ddt import ddt, data, unpack
import os, sys

from database.myentrez import myEntrez


DIR_BIN = "F:\\bio_broker\\bin"
DIR_CACHE = "F:\\bio_broker\\cache"
DIR_DOWNLOAD = "F:\\bio_broker\\download"


@ddt
class Test_(TestCase):

    def setUp(self):
        pass

    def test_get_db_infos(self):
        res = myEntrez().get_db_infos()
        pubmed = res['pubmed']
        assert pubmed['DbName'] == 'pubmed'
        assert int(pubmed['Count']) >1e6
        update = datetime.strptime(pubmed['LastUpdate'], "%Y/%m/%d %H:%M")
        assert update < datetime.now()