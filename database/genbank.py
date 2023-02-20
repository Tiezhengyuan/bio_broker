"""
GenBank: 
"""
import os, sys
from bs4 import BeautifulSoup
from Bio import Entrez

from connector.http import HTTP
from utils.threading import Threading
from database.myentrez import myEntrez

class GenBank(myEntrez):
    db = 'nucleotide'

    def __init__(self):
        super(GenBank, self).__init__()
        self.endpoint = 'https://eutils.ncbi.nlm.nih.gov/entrez/'


    def search_genbank(self, term:str, **kwargs):
        '''
        retrieve 20 accession number per time
        itype: acc, gi
        '''
        idtype = kwargs['idtype'] if 'idtype' in kwargs else 'acc'
        return self.search_entrez(
            db=self.db,
            term=term,
            idtype=idtype
        )
    
    def retrieve_records(self, id_list:list, **kwargs)->dict:
        '''
        rettype: gb, fasta, gp, etc
        retmode: text, xml, etc
        '''
        rettype = kwargs['rettype'] if 'rettype' else 'gb'
        retmode = kwargs['retmode'] if 'retmode' else 'text'
        records = {}
        for id in id_list:
            rec = self.retrieve_record(
                db=self.db,
                id=id,
                rettype=rettype,
                retmode=retmode
            )
            records[id] = rec
        return records



