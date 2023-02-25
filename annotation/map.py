
from typing import Iterable
import os
import json
from utils.commons import Commons
from utils.utils import Utils
from utils.file import File
from utils.dir import Dir
from utils.handle_json import HandleJson

class Map(Commons):
    def __init__(self):
        super(Map, self).__init__()
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
                        if isinstance(term[target_term], list):
                            map[uid] += term[target_term]
                        else:
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
        #save map
        self.save_map_cache(map, 'GeneID', target_term)
        self.save_map_cache(rev_map, target_term, 'GeneID')
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
                        if isinstance(k, list):
                            for sub in k:
                                Utils.update_dict(map, sub, v)    
                        else:
                            Utils.update_dict(map, str(k), v)
        #save map
        self.save_map_cache(map, key1, key2)
        return map

    def save_map_cache(self, map:dict, key1:str, key2:str)->str:
        '''
        save map in dictionary to cache directory
        '''
        outfile = os.path.join(self.dir_cache, f"{key1}_{key2}.json")
        HandleJson(outfile).save_json(map)
        local_cache_path = HandleJson(self.json_cache).to_dict()
        Utils.init_dict(local_cache_path, ['map', key1, key2])
        local_cache_path['map'][key1][key2] = outfile
        HandleJson(self.json_cache).save_json(local_cache_path)
        return outfile   

    def read_map_cache(self, key1:str, key2:str)->Iterable:
        '''
        read map cache
        '''
        c = HandleJson(self.json_cache)
        json_path = c.search_value(['map', key1, key2])
        return HandleJson(json_path).read_json()