"""
PubMed: https://pubmed.ncbi.nlm.nih.gov/
"""
import os, sys
from bs4 import BeautifulSoup
import wget

from connector.http import HTTP
from utils.threading import Threading

class PubMed:
    def __init__(self):
        self.endpoint = 'https://eutils.ncbi.nlm.nih.gov/entrez/'
        self.dir_download = os.environ.get('DIR_DOWNLOAD')
        self.dir_bin = os.environ.get('DIR_BIN')
        self.ref = {}
    
    def process(self, pmid:str):
        '''
        download article in PDF format
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
            local_file = os.path.join(self.dir_download, f"{self.ref.get('pmid', '')}_{file_name}")
            HTTP().download_pdf(i['content'], local_file)
            links.append({
                'pdf_url': i['content'],
                'local_path': local_file,
            })
        self.ref['pdf_links'] = links
        return links
            


