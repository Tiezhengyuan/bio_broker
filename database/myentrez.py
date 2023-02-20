"""
Entrez: https://eutils.ncbi.nlm.nih.gov
"""
from datetime import datetime
import os, sys
from bs4 import BeautifulSoup
import wget
from Bio import Entrez
# Entrez.api_key = "MyAPIkey"
Entrez.email = "tiezhengyuan@hotmail.com"

from connector.http import HTTP
from utils.threading import Threading

class myEntrez:
    def __init__(self):
        # self.endpoint = 'https://eutils.ncbi.nlm.nih.gov/entrez/'
        self.dir_download = os.environ.get('DIR_DOWNLOAD', '')
        self.dir_bin = os.environ.get('DIR_BIN', '')
    
    def get_db_infos(self):
        db_infos = {}
        handle = Entrez.einfo()
        record = Entrez.read(handle)
        for db in record["DbList"]:
            db_handle = Entrez.einfo(db=db)
            db_info = Entrez.read(db_handle)['DbInfo']
            # print(db_info)
            db_infos[db] = db_info
        return db_infos

    def search_entrez(self, db:str, term:str, **kwargs):
        '''
        retrieve 20 ids per time
        '''
        ret_start = 0
        while ret_start is not None:
            handle = Entrez.esearch(
                db=db,
                term = term,
                RetStart=ret_start
            )
            record = Entrez.read(handle)
            ret_start += 20
            if int(record['Count']) < ret_start:
                ret_start = None
            yield record['IdList']