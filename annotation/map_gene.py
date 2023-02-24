'''
Map Gene 
'''
import os
import json
from utils.commons import Commons
from utils.file import File
from utils.dir import Dir
from utils.utils import Utils

class MapGene(Commons):

    def __init__(self):
        super(MapGene, self).__init__()
        self.dir_map = os.path.join(self.dir_cache, 'map')

    def get_map(self, file_name:str, target_term:str)->tuple:
        '''
        gene uid ~ <terms>
        Note: local cache should exist
        '''
        map, rev_map = {}, {}
        tax_id = file_name.split('_', 2)[0]
        indir = Dir.cascade_dir(self.dir_map, tax_id, self.cascade_num)
        infile = os.path.join(indir, file_name)
        with open(infile, 'r') as f:
            data = json.load(f)
            for uid, terms in data.items():
                map[uid] = [] 
                for term in terms:
                    if term.get(target_term) not in (map[uid], '-', None):
                        map[uid].append(term[target_term])
                        break
        # reverse mapping and remove duplicates
        for term, vals in map.items():
            for v in vals:
                if v in rev_map:
                    if uid not in rev_map[v]:
                        rev_map[v].append(uid)
                else:
                    rev_map[v] = []
        return (map, rev_map)


    def get_intra_map(self, file_name:str, key1:str, key2:str)->dict:
        '''
        map key1~key2 within the uid list
        '''
        map = {}
        tax_id = file_name.split('_', 2)[0]
        indir = Dir.cascade_dir(self.dir_map, tax_id, self.cascade_num)
        infile = os.path.join(indir, file_name)
        with open(infile, 'r') as f:
            data = json.load(f)
            for terms in data.values():
                for term in terms:
                    if key1 in term and key2 in term:
                        k, v = term[key1], term[key2]
                        if k != '-' and k not in map:
                            map[k] = []
                        if k in map and v not in map[k]:
                            map[k].append(v)
        return map

    def geneid_to_symbol(self, tax_id:str):
        '''
        geneid ~ gene symbols
        '''
        return self.get_map(f"{tax_id}_gene2accession.json", 'Symbol')