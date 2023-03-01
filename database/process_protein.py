'''
process gene/DATA
'''
from copy import deepcopy
import itertools
import os
import json
from typing import Iterable, Callable
from utils.commons import Commons
from utils.file import File
from utils.dir import Dir
from utils.utils import Utils
from utils.jtxt import Jtxt
from utils.handle_json import HandleJson
from database.swissprot import Swissprot
from database.process_gene import ProcessGene


class ProcessProtein(Commons):
    
    def __init__(self):
        super(ProcessProtein, self).__init__()
        self.expasy_file = os.path.join(self.dir_cache, 'expasy.tjxt')
    def process_protein(self):
        '''
        protein annotations
        '''
        # startup: Uniprot-Sprot
        # with open(self.expasy_file, 'wt') as f:
        #     handle = Swissprot().parse_protein()
        #     for rec in handle:
        #         # print(json.dumps(rec))
        #         f.write(json.dumps(rec)+'\n')
        
        # parse NCBI protein accession
        self.parse_ncbi_protein()

    def parse_ncbi_protein(self):
        step = 10000
        tmp = self.expasy_file + '.tmp'
        with open(tmp, 'wt') as f:
            handle = Jtxt(self.expasy_file).read_jtxt()
            range = [0, step]
            data, acc_pair = self.get_acc_slice(handle, range)
            while acc_pair:
                print(range)
                ProcessGene().parse_ncbi_acc(acc_pair)
                self.update_acc(data, acc_pair, f)
                range = [ i + step for i in range ]
                data, acc_pair = self.get_acc_slice(handle, range)
        # os.remove(self.expasy_file)
        # os.rename(tmp, self.expasy_file)

    
    def get_acc_slice(self, handle:Iterable, range:list):
        data, acc_pair = [], {}
        for rec in itertools.islice(handle, range[0], range[1]):
            data.append(rec)
            for item in rec.get('accessions', []):
                if item.get('UniProtKB_protein_accession', '-') != '-':
                    acc_pair[item['UniProtKB_protein_accession']] = []
        return data, acc_pair

    def update_acc(self, data:tuple, acc_pair:dict, file_handle):
        for rec in data:
            for item in rec.get('accessions', []):
                target = item.get('UniProtKB_protein_accession')
                if target in acc_pair:
                    Utils.update_dict(item, "protein_accession.version", acc_pair[target])
            file_handle.write(json.dumps(rec) + '\n')

