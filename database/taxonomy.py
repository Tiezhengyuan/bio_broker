"""
taxonomy data from https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/
"""
import json
import os
from zipfile import ZipFile
import xml.etree.ElementTree as et

from connector.connect_ftp import ConnectFTP
from database.ncbi_entrez import NCBIEntrez
from utils.commons import Commons
from utils.dir import Dir
from utils.file import File
from utils.utils import Utils


class Taxonomy(NCBIEntrez):
    db = 'taxonomy'

    def __init__(self):
        super(Taxonomy, self).__init__()
        self.endpoint = 'ftp.ncbi.nlm.nih.gov'
        self.download_path = os.path.join(self.dir_download, 'NCBI', 'taxonomy')        
    
    def download_taxonomy(self):
        '''
        https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.zip
        '''
        # download
        file_name = 'new_taxdump.zip'
        Dir(self.download_path).init_dir()
        ConnectFTP(self.endpoint).download_file(
            'pub/taxonomy/new_taxdump/',
            file_name,
            self.download_path
        )
        #unzip
        try:
            local_file = os.path.join(self.download_path, file_name)
            with ZipFile(local_file, "r") as f:
                f.extractall(self.download_path)
        except Exception as e:
            # print(e)
            return False
        return True
    
    def get_taxonomy(self):
        '''
        Note: nodes.dmp should exist
        '''
        taxonomy = {}

        # read names.dmp
        name_file = os.path.join(self.download_path, 'names.dmp')
        col = ['tax_id', 'name_txt', 'unique_name', 'name_class']
        handle = File(name_file).read_dump_file()
        for items in handle:
            rec = {k:v for k,v in zip(col, items)}
            tax_id = rec['tax_id']
            Utils.init_dict(taxonomy, [tax_id,'names'], [])
            taxonomy[tax_id]['tax_id'] = tax_id
            del rec['tax_id']
            taxonomy[tax_id]['names'].append(rec)
        
        # #read nodes.dmp
        # name_file = os.path.join(self.download_path, 'nodes.dmp')
        # col = ['tax_id', 'parent_tax_id', 'rank', 'embl_code', 'division_id',
        #         'inherited_div_flag','genetic_code_id','inherited_GC_flag',
        #         'mitochondrial_genetic_code_id','inherited_MGC_flag',
        #         'GenBank_hidden_flag','hidden_subtree_root_flag','comments',
        #         'plastid_genetic_code_id','inherited_PGC_flag',
        #         'specified_species','hydrogenosome_genetic_code_id',
        #         'inherited_HGC_flag',
        # ]
        # handle = File(name_file).read_dump_file()
        # for items in handle:
        #     rec = {k:v for k,v in zip(col, items)}
        #     tax_id = rec['tax_id']
        #     Utils.init_dict(taxonomy, [tax_id,'nodes'], [])
        #     taxonomy[tax_id]['tax_id'] = tax_id
        #     del rec['tax_id']
        #     taxonomy[tax_id]['nodes'].append(rec)

        #export 
        outfile = os.path.join(self.dir_cache, 'taxonomy.json')
        File(outfile).save_json(taxonomy)
    
    def search_by_tax_id(self, tax_id:str):
        '''
        retrieve taxonomy using tax_id from efetch
        '''
        taxonomy = {}
        res = self.efetch(db=self.db, id=tax_id, retmode='xml')
        # self.print_xml(res)
        root = et.fromstring(res)
        for c1 in root:
            for c2 in c1:
                taxonomy[c2.tag] = c2.text.rstrip()
                # print(c2, c2.tag, c2.text)
        return taxonomy