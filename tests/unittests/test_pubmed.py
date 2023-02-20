'''
Test class 
'''
from unittest import TestCase, mock, skip
from ddt import ddt, data, unpack
import os, sys

from database.pubmed import PubMed

DIR_BIN = "F:\\bio_broker\\bin"
DIR_CACHE = "F:\\bio_broker\\cache"
DIR_DOWNLOAD = "F:\\bio_broker\\download"

@ddt
class Test_(TestCase):

    def setUp(self):
        pass

    @skip
    @data(
        # Silverchair Information Systems
        [19880848, ],
        # Highwire
        [32563999, ],
    )
    @unpack
    def test_get_outerlink(self, pmid):
        '''
        example url: 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&id=19880848&cmd=prlinks'
        '''
        par = {
            'dbfrom': 'pubmed',
            'id': pmid,
            'cmd': 'prlinks',
        }
        res = PubMed().get_outerlink('eutils/elink.fcgi/', par)
        # print(res)
        assert res.get('pmid') == par['id']
    
    @skip
    @mock.patch.dict(os.environ, {"DIR_DOWNLOAD": DIR_DOWNLOAD, "DIR_BIN": DIR_BIN})
    def test_get_pdf(self):
        url = 'https://academic.oup.com/eurheartj/article/30/23/2838/476786'
        res = PubMed().get_pdf(url)
        assert list(res[0]) == ['pdf_url', 'local_path']


    @data(
        # Silverchair Information Systems
        [19880848, ],
        # Highwire
        [32563999, ],
    )
    @unpack
    @mock.patch.dict(os.environ, {"DIR_DOWNLOAD": DIR_DOWNLOAD, "DIR_BIN": DIR_BIN})
    def test_process(self, pmid):
        PubMed().process(pmid)
