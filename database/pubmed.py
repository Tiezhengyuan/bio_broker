"""
PubMed: https://pubmed.ncbi.nlm.nih.gov/
"""
import os, sys
from bs4 import BeautifulSoup
from Bio import Entrez

from connector.http import HTTP
from utils.threading import Threading
from database.myentrez import myEntrez

class PubMed(myEntrez):
    db = 'pubmed'

    def __init__(self):
        super(PubMed, self).__init__()
        self.endpoint = 'https://eutils.ncbi.nlm.nih.gov/entrez/'
        self.ref = {}

    def get_ref(self):
        return self.ref

    def process(self, pmid:str):
        '''
        download article in PDF format
        pmid is parsing medline records
        '''
        par = {
            'dbfrom': 'pubmed',
            'id': pmid,
            'cmd': 'prlinks',
        }
        self.get_outerlink('eutils/elink.fcgi/', par)
        self.get_pdf(self.ref['outer_url'])

    def get_outerlink(self, path:str, par:dict):
        text_data = HTTP(self.endpoint).retrieve_data(path, par)
        soup = BeautifulSoup(text_data, 'html.parser')
        s1=soup.idurlset.objurl
        outerlink = {
            'pmid': par['id'],
            'outer_url': s1.url.get_text(),
            'ref_category': s1.category.get_text(),
            'provider_abbr': s1.provider.nameabbr.get_text(),
            'provider_id': s1.provider.id.get_text(),
        }
        self.ref.update(outerlink)
        return outerlink
    
    def get_pdf(self, outerlink:str):
        links = []
        text_data = HTTP(outerlink).retrieve_data()
        soup = BeautifulSoup(text_data, 'html.parser')
        for i in soup.find_all('meta',attrs={'name':'citation_pdf_url'}):
            # print(i['content'])
            file_name = os.path.basename(i['content'])
            local_file = os.path.join(self.dir_download, \
                f"{self.ref.get('pmid', '')}_{file_name}")
            HTTP().download_pdf(i['content'], local_file)
            links.append({
                'pdf_url': i['content'],
                'local_path': local_file,
            })
        self.ref['pdf_links'] = links
        return links
            
    def search_pubmed(self, term:str, **kwargs):
        '''
        retrieve 20 pmids per time
        '''
        idtype = kwargs['idtype'] if 'idtype' in kwargs else 'pmid'
        return self.search_entrez(
            db=self.db,
            term=term,
            idtype=idtype
        )
    
    def search_citations(self, pmid:str):
        '''
        search citations
        '''
        res= self.fetch_elink(
            dbfrom=self.db,
            db="pmc",
            link_name="pubmed_pmc_refs",
            id=pmid
        )[0]
        if res['ERROR'] == [] and len(res['LinkSetDb']) > 0:
            pmc_ids = [link["Id"] for link in res["LinkSetDb"][0]["Link"]]
            return pmc_ids
        return []
