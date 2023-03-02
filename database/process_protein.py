'''
process gene/DATA
'''
from copy import deepcopy
import itertools
import os
import json
from typing import Iterable, Callable
import pandas as pd

from utils.commons import Commons
from utils.file import File
from utils.dir import Dir
from utils.utils import Utils
from utils.jtxt import Jtxt
from utils.handle_json import HandleJson
from database.swissprot import Swissprot
from database.process_gene import ProcessGene


class ProcessProtein(Commons):
    
    def __init__(self, debugging:bool=None):
        super(ProcessProtein, self).__init__()
        self.debugging = False if debugging is None else True
        self.expasy_file = os.path.join(self.dir_cache, 'expasy.tjxt')
    def process_protein(self):
        '''
        protein annotations
        '''
        # startup: Uniprot-Sprot
        with open(self.expasy_file, 'wt') as f:
            handle = Swissprot().parse_protein()
            for rec in handle:
                # print(json.dumps(rec))
                f.write(json.dumps(rec)+'\n')
        
        # parse NCBI protein accession
        self.parse_ncbi_protein()

    def parse_ncbi_protein(self):
        # get Series of ncbi accessions
        accessions = ProcessGene().parse_acc(name_index=1)

        # scan
        tmp = self.expasy_file + '.tmp'
        with open(tmp, 'wt') as f:
            handle = Jtxt(self.expasy_file).read_jtxt()
            for rec in handle:
                for item in rec.get('accessions', []):
                    if item.get('UniProtKB_protein_accession', '-') != '-':
                        matched = accessions.get(item['UniProtKB_protein_accession'])
                        if matched is not None:
                            matched = list(matched) if type(matched)==pd.Series else [matched,]
                            Utils.update_dict(item, "protein_accession.version", matched)
                            print('##matched', item)
                f.write(json.dumps(rec) + '\n')
        if self.debugging is False:
            os.remove(self.expasy_file)
            os.rename(tmp, self.expasy_file)
