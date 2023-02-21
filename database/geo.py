"""
Gene Expression Omnibus: a data repository of 
high-throughput gene expression and hybridization array data. 
""" 
import os, sys, re
from bs4 import BeautifulSoup
from Bio import Entrez

from connector.http import HTTP
from utils.threading import Threading
from database.myentrez import myEntrez

class GEO(myEntrez):
    db = 'gds'

    def __init__(self):
        super(GEO, self).__init__()

    def search_geo(self, term:str, **kwargs):
        '''
        retrieve 20 UID per time
        '''
        idtype = kwargs['idtype'] if 'idtype' in kwargs else 'uid'
        return self.search_entrez(
            db=self.db,
            term=term
        )
    
    def retrieve_records(self, id_list:list, **kwargs)->dict:
        '''
        
        '''
        records = {}
        for id in id_list:
            rec = self.retrieve_record(
                db=self.db,
                id=id
            )
            print(rec)
            items = rec.split('\n')
            summary = {
                'uid': id,
                'title': items[1],
                'abstract': items[2],
                'organism': ','.join(re.findall(r'Organism:\t+(.*)', rec)),
                'type': ','.join(re.findall(r'Type:\t+(.*)', rec)),
                'platform': ','.join(re.findall(r'Platform:[\t+|\s+](.*)', rec)),
                'ftp': ','.join(re.findall(r'FTP download:[\s+]GEO[\s+]ftp://(.*)', rec)),
                'series_samples': ','.join(re.findall(r'Series[\t+|\s+](\w*)', rec)),
                'accession': ','.join(re.findall(r'Accession:[\t+|\s+](\w*)', rec)),
            }
        return records



