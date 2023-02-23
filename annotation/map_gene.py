'''
Map Gene 
'''
import os
import json
import pandas as pd
from utils.commons import Commons
from utils.file import File
from utils.dir import Dir
from utils.utils import Utils

class MapGene(Commons):
    def __init__(self):
        super(MapGene, self).__init__()
    
    def gene_to_acc(self):
        '''
        Map Entrez Gene identifiers(uid) to GenBanck Accession Numbers
        Note: local file should exist
        '''
        map, tax_id, file_name = {}, '', 'gene2accession'
        # local file is downloaded from NCBI FTP
        mapfile = os.path.join(self.dir_download, 'NCBI', \
            'gene', 'DATA', f"{file_name}.gz")
        # get column names
        header = File(mapfile).read_top_lines()[0]
        col_names = header.split('\t')
        for lines in File(mapfile).read_slice(1e5, 1):
            map = {}
            for line in lines:
                items = line.rstrip().split('\t')
                tax_id, geneid = items[0], items[1]
                Utils.init_dict(map, [tax_id, geneid], [])
                map[tax_id][geneid].append(
                    {k:v for k,v in zip(col_names, items)}
                )
                # print(map[tax_id][geneid])
            # save map to cache
            for tax_id in map:
                outdir = os.path.join(self.dir_cache, 'map', tax_id)
                print(outdir)
                Dir(outdir).init_dir()
                outfile = os.path.join(outdir, f"{file_name}.json")
                File(outfile).update_json(map[tax_id])



        
