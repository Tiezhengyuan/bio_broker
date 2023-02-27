'''
process gene/DATA
'''
import os
import json
from typing import Iterable, Callable
from utils.commons import Commons
from utils.file import File
from utils.dir import Dir
from utils.utils import Utils
from utils.jtxt import Jtxt
from utils.handle_json import HandleJson

class ProcessGene(Commons):

    def __init__(self):
        super(ProcessGene, self).__init__()
        # store local file is downloaded from NCBI FTP
        self.dir_source = os.path.join(self.dir_download, \
            'NCBI', 'gene', 'DATA')
        

    def process_map(self, tax_id:str):
        '''
        process *.gz and store map in cache
        '''
        # create new json in cache dir
        # file_names = ['gene2accession', 'gene2refseq', 'gene2pubmed', \
        #     'gene2go', 'gene2ensembl', ]
        # for file_name in file_names:
        #     self.map_taxonomy_gene(file_name, tax_id)
        
        # self.parse_orthologs(tax_id)
        # self.parse_neighbors(tax_id)
        # self.parse_info(tax_id)
        # self.parse_history(tax_id)
        # self.parse_group(tax_id)
        # # TODO: debugging needed
        #parse and save in map cache
        self.parse_uniprotkb()

    def gene_to_accession(self, tax_id:str=None, func:Callable=None):
        '''
        Map Entrez Gene identifiers(uid) to GenBanck Accession Numbers
        source file: gene2accession.gz
        '''
        if tax_id is None:
            self.map_gene('gene2accession')
        else:
            self.map_taxonomy_gene('gene2accession', tax_id, func)

    def gene_to_refseq(self, tax_id:str=None):
        '''
        Map Entrez Gene identifiers(uid) to Accession Numbers of references
        source file: gene2refseq.gz
        '''
        if tax_id is None:
            self.map_gene('gene2refseq')
        else:
            self.map_taxonomy_gene('gene2refseq', tax_id)

    def gene_to_pubmed(self, tax_id:str=None):
        '''
        Map Entrez Gene identifiers(uid) to PubMed_ID
        source file: gene2pubmed.gz
        '''
        if tax_id is None:
            self.map_gene('gene2pubmed')
        else:
            self.map_taxonomy_gene('gene2pubmed', tax_id)

    def gene_to_go(self, tax_id:str=None):
        '''
        Map Entrez Gene identifiers(uid) to GO
        source file: gene2go.gz
        '''
        if tax_id is None:
            self.map_gene('gene2go')
        else:
            self.map_taxonomy_gene('gene2go', tax_id)

    def gene_to_ensembl(self, tax_id:str=None):
        '''
        Map Entrez Gene identifiers(uid) to Ensembl
        source file: gene2ensembl.gz
        '''
        if tax_id is None:
            self.map_gene('gene2ensembl')
        else:
            self.map_taxonomy_gene('gene2ensembl', tax_id)

    def map_gene(self, file_name:str):
        '''
        Map Entrez Gene identifiers(uid) to some identifiers
        Note: local file should exist
        source file is downloaded from FTP
        '''
        map, tax_id = {}, '',
        # local file is downloaded from NCBI FTP
        mapfile = os.path.join(self.dir_source, f"{file_name}.gz")
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
            # save map to cache
            for tax_id in map:
                outdir = Dir.cascade_dir(self.dir_map, tax_id, self.cascade_num)
                Dir(outdir).init_dir()
                outfile = os.path.join(outdir, f"{tax_id}_{file_name}.jtxt")
                Jtxt(outfile).save_jtxt(map[tax_id])

    def map_taxonomy_gene(self, file_name:str, tax_id:str, func:Callable=None):
        '''
        Gieven a taxonomy
        Map Entrez Gene identifiers(uid) to some identifiers 
        Note: local file should exist
        source file is downloaded from FTP
        '''
        map = {}
        # local file is downloaded from NCBI FTP
        mapfile = os.path.join(self.dir_source, f"{file_name}.gz")
        with File(mapfile).readonly_handle() as f:
            # get column names
            header = next(f).rstrip()
            col_names = header.split('\t')
            for line in f:
                items = line.rstrip().split('\t')
                this_tax_id, geneid = items[0], items[1]
                if this_tax_id == tax_id:
                    rec = {k:v for k,v in zip(col_names, items)}
                    if func is not None:
                        func(rec)
                    if geneid not in map:
                        map[geneid] = []
                    map[geneid].append(rec)
            # save map to cache
            outdir = Dir.cascade_dir(self.dir_map, tax_id, self.cascade_num)
            Dir(outdir).init_dir()
            outfile = os.path.join(outdir, f"{tax_id}_{file_name}.jtxt")
            Jtxt(outfile).save_jtxt(map)
                           
    def parse_uniprotkb(self):
        '''
        parse NCBI_protein_accession ~ UniProtKB_protein_accession
        source file: *_gene_refseq_uniprotkb_collab.gz
        '''
        outfile = os.path.join(self.dir_map, "gene_refseq_uniprotkb_collab.jtxt")
        infile = os.path.join(self.dir_source, "gene_refseq_uniprotkb_collab.gz")
        with File(infile).readonly_handle() as f:
            # skip the first line
            map = {}
            header = next(f)
            print(header.rstrip().split('\t'))
            for line in f:
                val1, val2 = line.rstrip().split('\t')
                # print(val1, val2)
                Utils.update_dict(map, val1, val2)
                if len(map) >= 1e3:
                    # append data as one line
                    Jtxt(outfile).append_jtxt(map)
                    # reset map
                    map = {}
            else:
                if map:
                    # append remaining data as one line
                    Jtxt(outfile).append_jtxt(map)
                        

    def parse_(self, tax_id:str, name:str, func:Callable=None):
        '''
        parse geneid ~ other info
        source file: gene_*.gz
        '''
        map = {}
        mapfile = os.path.join(self.dir_source, f"{name}.gz")
        with File(mapfile).readonly_handle() as f:
            col_names = next(f).strip().split('\t')
            for line in f:
                items = line.rstrip().split('\t')
                if tax_id == items[0]:
                    rec = {}
                    for k,v in zip(col_names, items):
                        rec[k] = v.split('|') if '|' in v else v
                    if func is not None:
                        func(rec)
                    Utils.update_dict(map, items[1], rec) 
        # save updated data
        outdir = Dir.cascade_dir(self.dir_map, tax_id, self.cascade_num)
        outfile = os.path.join(outdir, f"{tax_id}_{name}.jtxt")
        Jtxt(outfile).save_jtxt(map)

    def parse_neighbors(self, tax_id:str):      
        '''
        parse geneid with chromsome locus
        source file: gene_neighbors.gz
        '''
        self.parse_(tax_id, 'gene_neighbors')

    def parse_orthologs(self, tax_id:str):      
        '''
        parse orthology bewteen geneids
        source file: gene_orthologs.gz
        '''
        self.parse_(tax_id, 'gene_orthologs')

    def parse_history(self, tax_id:str):
        '''
        parse geneid with gene history
        source file: gene_history.gz
        '''
        self.parse_(tax_id, 'gene_history')

    def parse_group(self, tax_id:str):
        '''
        parse geneid with gene group
        source file: gene_group.gz
        '''
        self.parse_(tax_id, 'gene_group')


    def parse_info(self, tax_id:str):
        '''
        parse geneid with gene info
        source file: gene_info.gz
        '''
        self.parse_(tax_id, 'gene_info', ProcessGene.parse_dbxrefs)

    @staticmethod
    def parse_dbxrefs(rec:dict):
        if rec.get("dbXrefs") not in (None, '-'):
            if isinstance(rec["dbXrefs"], str):
                rec["dbXrefs"] = [rec["dbXrefs"],]
            for item in rec["dbXrefs"]:
                name, id = item.split(':', 1)
                Utils.update_dict(rec, name, id)
