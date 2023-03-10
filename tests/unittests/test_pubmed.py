'''
Test class 
'''
from tests.helper import *
from database.pubmed import PubMed


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
    @mock.patch.dict(os.environ, env)
    def test_get_pdf(self):
        url = 'https://academic.oup.com/eurheartj/article/30/23/2838/476786'
        res = PubMed().get_pdf(url)
        assert list(res[0]) == ['pdf_url', 'local_path']

    @skip
    @data(
        # Silverchair Information Systems
        [19880848, ],
        # Highwire
        [32563999, ],
    )
    @unpack
    @mock.patch.dict(os.environ, env)
    def test_process(self, pmid):
        PubMed().process(pmid)


    @skip
    @data(
        # ["bioinformatics[title]", 100],
        # ["human[Orgn] AND matK[Gene]", 100],
        ['Bioinformatics[journal] AND 2023/02[mindate]', 100]
    )
    @unpack
    def test_search_pubmed(self, term, expect):
        res = PubMed().search_pubmed(term, idtype='pmid')
        for i in res:
            print(i)

    @skip
    @data(
        ["14630660", 94],
        # wrong pmid
        ["0000", 0],
    )
    @unpack
    def test_search_citations(self, pmid, expect):
        res = PubMed().search_citations(pmid)
        assert len(res) >= expect