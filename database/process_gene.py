'''
process gene/DATA
'''
from copy import deepcopy
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
from connector.connect_redis import ConnectRedis

class ProcessGene(Commons):
    db = 'entrez'
    
    def __init__(self):
        super(ProcessGene, self).__init__()
        # store local file is downloaded from NCBI FTP
        self.dir_source = os.path.join(self.dir_download, \
            'NCBI', 'gene', 'DATA')
        

    def process_taxonomy_entrez(self, tax_id:str):
        '''
        process *.gz and store map in cache
        '''
        outdir = Dir.cascade_dir(self.dir_map, tax_id, self.cascade_num)
        Dir(outdir).init_dir()
        outfile = os.path.join(outdir, f"{tax_id}_{self.db}.jtxt")
        
        #parse and integrate gene data
        # file_names = ['gene2accession', 'gene2refseq', 'gene2pubmed', \
        #     'gene2go', 'gene2ensembl', 'gene_info', 'gene_group', \
        #     'gene_history', 'gene_neighbors', 'gene_orthologs', ]
        # for file_name in file_names[5:]:
        #     print(file_name)
        #     map = self.parse_taxonomy_gene2(file_name, tax_id)
        #     # save map to cache
        #     for m in map:
        #         Jtxt(outfile).merge_jtxt('GeneID', m)
        
        # self.format_gene(outfile)

        # parse uniprotkb
        self.parse_uniprotkb(outfile)

    def parse_taxonomy_gene2(self, file_name:str, tax_id:str)->Iterable:
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
            if header.startswith('#'): header = header[1:]
            col_names = header.split('\t')
            # print(col_names)
            for line in f:
                items = line.rstrip().split('\t')
                this_tax_id, geneid = items[0], items[1]
                if this_tax_id == tax_id:
                    if geneid not in map:
                        map[geneid] = {
                            col_names[0]: this_tax_id,
                            col_names[1]: geneid,
                            file_name: [],
                        }
                    rec = {}
                    for k,v in zip(col_names[2:], items[2:]):
                        rec[k] = v.split('|') if '|' in v else v
                    map[geneid][file_name].append(rec)
                # export
                if len(map) >= 1e4:
                    output = deepcopy(map)
                    map = {}
                    yield output
            else:
                if map:
                    yield map

    def format_gene(self, outfile:str):
        tmp = outfile + '.tmp'
        with open(tmp, 'wt') as f:
            handle = Jtxt(outfile).read_jtxt()
            for rec in handle:
                for info_rec in rec.get("gene_info", []): 
                    ProcessGene.format_dbxrefs(info_rec)
                for go_rec in rec.get("gene2go", []):
                    if '|' in go_rec["PubMed"]:
                        go_rec["PubMed"] = go_rec["PubMed"].split('|')
                    elif go_rec["PubMed"] == '-':
                        go_rec["PubMed"] = []
                    else:
                        go_rec["PubMed"] = [go_rec["PubMed"],]
                # print(json.dumps(rec.get("gene2go", []), indent=4))
                if rec:
                    f.write(json.dumps(rec)+'\n')
        os.remove(outfile)
        os.rename(tmp, outfile)


    @staticmethod
    def format_dbxrefs(rec:dict):
        if rec.get("dbXrefs") not in (None, '-'):
            if isinstance(rec["dbXrefs"], str):
                rec["dbXrefs"] = [rec["dbXrefs"],]
            for item in rec["dbXrefs"]:
                name, id = item.split(':', 1)
                Utils.update_dict(rec, name, id)


    def parse_uniprotkb(self, outfile:str):
        #initialize acc_pair
        acc_pair = {}
        handle = Jtxt(outfile).read_jtxt()
        for rec in handle:
            for key1 in ("gene2accession", "gene2refseq", "gene2ensembl"):
                for item in rec.get(key1, []):
                    pro_acc = item.get("protein_accession.version", '-')
                    if pro_acc != '-':
                        acc_pair[pro_acc] = []

        # parse acc_pair
        infile = os.path.join(self.dir_source, "gene_refseq_uniprotkb_collab.gz")
        with File(infile).readonly_handle() as f:
            # skip the first line
            _ = next(f)
            for line in f:
                val1, val2 = line.rstrip().split('\t')
                if val1 in acc_pair and val2 not in acc_pair[val1]:
                    acc_pair[val1].append(val2)
        
        #update outfile
        tmp = outfile + '.tmp'
        with open(tmp, 'wt') as f:
            handle = Jtxt(outfile).read_jtxt()
            for rec in handle:
                for key1 in ("gene2accession", "gene2refseq", "gene2ensembl"):
                    for item in rec.get(key1, []):
                        pro_acc = item.get("protein_accession.version", '-')
                        if pro_acc != '-' and pro_acc in acc_pair:
                            Utils.update_dict(
                                item,
                                'UniProtKB_protein_accession',
                                acc_pair[pro_acc]
                            )
                            # print(json.dumps(rec[key1], indent=4))
                if rec:
                    f.write(json.dumps(rec)+'\n')
            os.remove(outfile)
            os.rename(tmp, outfile)

    def get_uniprotkb(self)->Iterable:
        '''
        map NCBI_protein_accession ~ UniProtKB_protein_accession
        source file: *_gene_refseq_uniprotkb_collab.gz
        '''
        map = {}
        infile = os.path.join(self.dir_source, "gene_refseq_uniprotkb_collab.gz")
        with File(infile).readonly_handle() as f:
            # skip the first line
            header = next(f)
            # print(header.rstrip().split('\t'))
            for line in f:
                val1, val2 = line.rstrip().split('\t')
                # print(val1, val2)
                Utils.update_dict(map, val2, val1)
                if len(map) >= 1e6:
                    output = deepcopy(map)
                    map = {}
                    yield output
            else:
                if map:
                    yield map


    def search_ncbi_acc(self, acc_pair:dict):
        '''
        map NCBI_protein_accession ~ UniProtKB_protein_accession
        source file: *_gene_refseq_uniprotkb_collab.gz
        '''
        infile = os.path.join(self.dir_source, "gene_refseq_uniprotkb_collab.gz")
        with File(infile).readonly_handle() as f:
            # skip the first line
            _ = next(f)
            for line in f:
                ncbi_acc, uniprot_acc = line.rstrip().split('\t')
                if uniprot_acc in acc_pair:
                    Utils.update_dict(acc_pair, uniprot_acc, ncbi_acc)

    def parse_acc(self, name_index:int=None)->pd.Series:
        '''
        value: NCBI_protein_accession, index: UniProtKB_protein_accession
        source file: *_gene_refseq_uniprotkb_collab.gz
        '''
        if name_index not in (0, 1): name_index = 1
        value_index = 1 - name_index
        infile = os.path.join(self.dir_source, "gene_refseq_uniprotkb_collab.gz")
        df = pd.read_csv(infile, sep='\t', header=0)
        series = df.iloc[:,value_index].squeeze()
        series.index =df.iloc[:,name_index]
        # print(series)
        return series


    def feed_redis(self):
        '''
        map NCBI_protein_accession ~ UniProtKB_protein_accession
        source file: *_gene_refseq_uniprotkb_collab.gz
        '''
        rs = ConnectRedis('uniprot_acc')
        infile = os.path.join(self.dir_source, "gene_refseq_uniprotkb_collab.gz")
        with File(infile).readonly_handle() as f:
            # skip the first line
            _ = next(f)
            for line in f:
                ncbi_acc, uniprot_acc = line.rstrip().split('\t')
                rec = {
                    'NCBI_protein_accession': [ncbi_acc,],
                    'UniProtKB_protein_accession': [uniprot_acc,],
                }
                rs.put_uniprotkb_acc(uniprot_acc, rec)

