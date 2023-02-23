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

    def gene_to_acc(self):
        '''
        Map Entrez Gene identifiers(uid) to GenBanck Accession Numbers
        source file: gene2accession.gz
        '''
        self.map_gene('gene2accession')

    def gene_to_refseq(self):
        '''
        Map Entrez Gene identifiers(uid) to Accession Numbers of references
        source file: gene2refseq.gz
        '''
        self.map_gene('gene2refseq')

    def gene_to_pubmed(self):
        '''
        Map Entrez Gene identifiers(uid) to Accession Numbers of references
        source file: gene2refseq.gz
        '''
        self.map_gene('gene2pubmed')


    def map_gene(self, file_name:str):
        '''
        Map Entrez Gene identifiers(uid) to some identifiers
        Note: local file should exist
        source file is downloaded from FTP
        '''
        map, tax_id = {}, '',
        # local file is downloaded from NCBI FTP
        mapfile = os.path.join(self.dir_download, 'NCBI', \
            'gene', 'DATA', f"{file_name}.gz")
        # get column names
        header = File(mapfile).read_top_lines()[0]
        col_names = header.split('\t')
        for lines in File(mapfile).read_slice(1e6, 1):
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
                outdir = Dir.cascade_dir(self.dir_map, tax_id, 2)
                Dir(outdir).init_dir()
                outfile = os.path.join(outdir, f"{tax_id}_{file_name}.json")
                File(outfile).update_json(map[tax_id])


