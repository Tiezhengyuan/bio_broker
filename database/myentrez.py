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

    def search_entrez(self, db:str, term:str, idtype:str=None):
        '''
        retrieve 20 ids per time
        '''
        ret_start = 0
        while ret_start is not None:
            handle = Entrez.esearch(
                db=db,
                term = term,
                RetStart=ret_start,
                idtype=idtype
            )
            record = Entrez.read(handle)
            ret_start += 20
            if int(record['Count']) < ret_start:
                ret_start = None
            yield record['IdList']


    def efetch(self, db:str, id:str, rettype:str=None,\
            retmode:str=None):
        try:
            handle = Entrez.efetch(
                db=db,
                id=id,
                rettype=rettype,
                retmode=retmode
            )
            # return instance of Record class
            return handle.read()
        except Exception as e:
            print('failed retrieve record from Entrez', e)

    def fetch_elink(self, dbfrom:str, db:str, link_name:str, id:str):
        handle = Entrez.elink(
            dbfrom=dbfrom,
            db=db,
            LinkName=link_name,
            id=id
        )
        return Entrez.read(handle)