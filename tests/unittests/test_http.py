'''
Test class 
'''
from unittest import TestCase, mock
from ddt import ddt, data, unpack
import os, sys
from connector.http import HTTP

DIR_CACHE = "F:\\bio_broker\\cache"
DIR_DOWNLOAD = "F:\\bio_broker\\download"

class Test_(TestCase):

    def setUp(self):
        pass

    @mock.patch.dict(os.environ, {"DIR_DOWNLOAD": DIR_DOWNLOAD})
    def test_download_pdf(self):
        endpoint = 'http://eutils.ncbi.nlm.nih.gov'
        url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&id=32563999&retmode=ref&cmd=prlinks'
        outfile = os.path.join(DIR_DOWNLOAD, 'article')
        HTTP().download_pdf(url, outfile)