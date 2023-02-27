
from typing import Iterable, Callable
import os
import json
from utils.commons import Commons
from utils.utils import Utils
from utils.file import File
from utils.dir import Dir
from utils.handle_json import HandleJson
from utils.jtxt import Jtxt

class Map(Commons):
    def __init__(self):
        super(Map, self).__init__()

    def get_map(self, file_name:str, target_term:str, func:Callable=None)->tuple:
        '''
        gene uid ~ <terms>
        Note: local cache should exist
        '''
        map, rev_map = {}, {}
        tax_id = file_name.split('_', 2)[0]
        tax_dir = Dir.cascade_dir(self.dir_map, tax_id, self.cascade_num)
        infile = os.path.join(tax_dir, file_name)
        handle = Jtxt(infile).read_jtxt()
        for uid, terms in handle:
            # print(uid, terms)
            rec = []
            for term in terms:
                if term.get(target_term) not in (rec, '-', None):
                    if isinstance(term[target_term], list):
                        rec += term[target_term]
                    else:
                        rec.append(term[target_term])
            map[uid] = rec if func is None else func(rec)
        # reverse mapping and remove duplicates
        for k, vals in map.items():
            for v in vals:
                if v in rev_map:
                    if k not in rev_map[v]:
                        rev_map[v].append(k)
                else:
                    rev_map[v] = [k,]
        #save map
        self.save_map_cache(map, ['taxonomy', tax_id, 'GeneID', target_term,], tax_dir)
        self.save_map_cache(rev_map, ['taxonomy', tax_id, target_term, 'GeneID',], tax_dir)
        return (map, rev_map)


    def get_intra_map(self, file_name:str, key1:str, key2:str)->dict:
        '''
        map key1~key2 within the uid list
        '''
        map = {}
        tax_id = file_name.split('_', 2)[0]
        tax_dir = Dir.cascade_dir(self.dir_map, tax_id, self.cascade_num)
        infile = os.path.join(tax_dir, file_name)
        handle = Jtxt(infile).read_jtxt()
        for _, terms in handle:
            for term in terms:
                if key1 in term and key2 in term:
                    k, v = term[key1], term[key2]
                    if isinstance(k, list):
                        for sub in k:
                            Utils.update_dict(map, sub, v)    
                    else:
                        Utils.update_dict(map, str(k), v)
        #save map
        self.save_map_cache(map, ['taxonomy', tax_id, key1, key2,], tax_dir)
        return map

    def map_term(self, handle:Iterable, key1:list, key2:list):
        '''
        map key1 ~ key2
        '''
        map = {}
        for rec in handle:
            val1 = Utils.get_deep_value(rec, key1)
            val2 = Utils.get_deep_value(rec, key2)
            # print(val1, val2)
            if val1 and val2:
                for k in val1:
                    map[k] = val2
        return map
    
    def save_map_cache(self, map:dict, keys:list, outdir:str=None)->str:
        '''
        save map in dictionary to cache directory
        '''
        if len(keys) < 2:
            return None
        # save map
        if outdir is None: outdir =  self.dir_cache
        Dir(outdir).init_dir()
        outfile = os.path.join(outdir, f"{keys[-2]}_{keys[-1]}.json")
        HandleJson(outfile).save_json(map)

        # update map path stored in self.json_cache
        local_cache_path = HandleJson(self.json_cache).to_dict()
        Utils.init_dict(local_cache_path, keys, outfile)
        HandleJson(self.json_cache).save_json(local_cache_path)
        return outfile   

    def read_map_cache(self, keys:list)->Iterable:
        '''
        read map cache using keys in list
        for example: {'a':{'b':4}}: keys = ['a', 'b'], return 4
        '''
        c = HandleJson(self.json_cache)
        json_path = c.search_value(keys)
        return HandleJson(json_path).read_json()

    def get_map_cache(self, keys:list)->dict:
        '''
        get map cache as dict
        '''
        c = HandleJson(self.json_cache)
        json_path = c.search_value(keys)
        try:
            with open(json_path[0], 'r') as f:
                return json.load(f)
        except Exception as e:
            print(e)
        return {}
