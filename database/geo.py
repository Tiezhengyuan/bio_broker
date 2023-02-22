"""
Gene Expression Omnibus: a data repository of 
high-throughput gene expression and hybridization array data. 
""" 
import os, sys, re
from bs4 import BeautifulSoup
from Bio import Entrez, Geo

from connector.http import HTTP
from connector.connect_ftp import ConnectFTP
from utils.threading import Threading
from database.myentrez import myEntrez

class GEO(myEntrez):
    db = 'gds'

    def __init__(self):
        super(GEO, self).__init__()
        self.ftp_endpoint = 'ftp.ncbi.nlm.nih.gov'
        self.dir_download = os.environ.get('DIR_DOWNLOAD')

    def retrieve_uids(self, term:str):
        '''
        get uids by GEO accession number
        those uids define: platform GPL..., sample GSM..., series GSE...
        retrieve 20 UID per time
        '''
        res = self.search_entrez(db=self.db, term=term)
        ids = sum(res, [])
        ids = sorted(list(set(ids)), key=int)
        return ids
    

    def retrieve_summary(self, id_list:list)->dict:
        '''
        all ids comes from one GSE 
        series GSE, platform: GPL, sample GSM
        '''
        geo = {'samples':[]}
        for id in id_list:
            rec = self.efetch(db=self.db, id=id)
            # print(repr(rec))
            # print(rec)
            acc = self.parse_accession(rec)
            if acc.startswith('GPL'):
                geo['platform'] = {
                    'uid': id,
                    'accession': acc,
                    'title': self.parse_title(rec),
                    'desc': self.parse_desc(rec),
                    'ftp_url': self.parse_ftp_url(rec),
                }
            elif  acc.startswith('GSE'):
                geo['organism'] = self.parse_organism(rec)
                geo['type'] = self.parse_type(rec)
                geo['series'] = {
                    'uid': id, 
                    'accession': acc,
                    'title': self.parse_title(rec),
                    'desc': self.parse_desc(rec),
                    'ftp_url': self.parse_ftp_url(rec),
                }
            else:
                geo['samples'].append({
                    'uid': id, 
                    'accession': acc,
                    'title': self.parse_title(rec),
                    'source_name': self.parse_source_name(rec),
                })
        return geo

    def parse_accession(self, rec:str):
        return ','.join(re.findall(r'Accession:[\t+|\s+](\w*)', rec))
    def parse_title(self, rec:str):
        return ','.join(re.findall(r'\n1.[\s+|\t+](.*)\n', rec))
    def parse_desc(self, rec:str):
        return ' '.join(re.findall(r'\(Submitter supplied\) (.*)', rec))
    def parse_organism(self, rec:str):
        return ','.join(re.findall(r'Organism:\t+(.*)', rec))
    def parse_type(self, rec:str):
        return ','.join(re.findall(r'Type:\t+(.*)', rec))
    def parse_platform(self, rec:str):
        return ','.join(re.findall(r'Platform:[\t+|\s+](.*)', rec))
    def parse_ftp_url(self, rec:str):
        return ','.join(re.findall(r'ftp://(.*)', rec))
    def parse_source_name(self, rec:str):
        return ','.join(re.findall(r'Source name:\s+(.*)', rec))
    def parse_samples(self, rec:str):
        return ','.join(re.findall(r'Series[\t+|\s+](\w*)', rec))

    def retrieve_geo_ftp_url(self, id_list:list):
        for id in id_list:
            rec = self.efetch(db=self.db, id=id)
            acc = self.parse_accession(rec)
            print(acc)
            if  acc.startswith('GSE'):
                print(rec)
                return self.parse_ftp_url(rec)

    def download_data(self, GSE:str):
        # get FTP path
        ids = self.retrieve_uids(GSE)
        ftp_url = self.retrieve_geo_ftp_url(ids)
        # print(ftp_url)

        # download data from FTP
        ftp_path = ftp_url.replace(self.ftp_endpoint, '')
        ConnectFTP(self.ftp_endpoint).download_tree(
            GSE, ftp_path, None)

