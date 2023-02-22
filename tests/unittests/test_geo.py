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
        ["GSE16[acc]", 27],
        # ["GSE152641[acc]", None],
    )
    @unpack
    def test_retrieve_uids(self, GSE, samples):
        res = GEO().retrieve_uids(GSE)
        print(res, len(res))

    @skip 
    @data(
        # [['200000016',],],
        [['100000028', '200000016','300000794','300000795',],],
    )
    @unpack
    def test_retrieve_summary(self, id_list):
        res = GEO().retrieve_summary(id_list)
        print(res)

    @data(
       ["GSE152641",],
    )
    @unpack
    @mock.patch.dict(os.environ, {'DIR_DOWNLOAD': DIR_DOWNLOAD})
    def test_download_data(self, GSE):
        res = GEO().download_data(GSE)

