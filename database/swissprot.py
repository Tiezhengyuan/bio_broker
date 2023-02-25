"""
UniProt: https://www.uniprot.org/
"""
from copy import deepcopy
import json
import os
from typing import Iterable
from Bio import SwissProt

from utils.commons import Commons
from utils.file import File
from utils.dir import Dir
from utils.utils import Utils
from utils.handle_json import HandleJson

class Swissprot(Commons):
    db = 'swiss-prot'

    def __init__(self)->None:
        super(Swissprot, self).__init__()
        self.dir_local = os.path.join(self.dir_download, 'expasy', self.db, 'release')
        self.cache_local = os.path.join(self.dir_cache, self.db)
        Dir(self.cache_local).init_dir()

    def process(self):
        metadata=(
            (['accessions',], ['taxonomy_id',], 'accession_taxonomy', "NCBI taxonomy"),
            (['accessions',], ['sequence',], 'accession_sequence', "protein sequence"),
            (['accessions',], ['cross_reference','EMBL', 'accession'], 'accession_EMBLacc', "EMBL-GenBank-DDBJ"),
            (['accessions',], ['cross_reference','GO', 'id'], 'accession_GO', 'GO'),
        )
        for key1, key2, filename, key2 in metadata:
            outfile = os.path.join(self.cache_local, f"{filename}.json")
            self.map_term(key1, key2, outfile)
            HandleJson(self.json_cache).update_json({
                'map': {"UniProtKB accession": {key2: outfile}}
            })

    def parse_protein(self)->Iterable:
        local_file = os.path.join(self.dir_local, 'uniprot_sprot.dat.gz')
        handle = File(local_file).readonly_handle()
        for record in SwissProt.parse(handle):
            rec = {
                'accessions': record.accessions,
                'entry_name': record.entry_name,
                'data_class': record.data_class,
                'molecule_type': record.molecule_type,
                'sequence_length': int(record.sequence_length),
                'created': {k:v for k,v in zip(('date', \
                    'release'), record.created)},
                'sequence_update': {k:v for k,v in zip(('date', \
                    'release'), record.sequence_update)},
                'annotation_update': {k:v for k,v in zip(('date', \
                    'release'), record.annotation_update)},
                'description': record.description,
                'gene_name': record.gene_name,
                'organism': record.organism,
                'organelle': record.organelle,
                'organism_classification': record.organism_classification,
                'taxonomy_id': record.taxonomy_id,
                'host':[{'host_organism':a, 'host_taxonomy_id':b,} for a,b \
                    in zip(record.host_organism, record.host_taxonomy_id)],
                'comments': record.comments,
                'keywords': record.keywords,
                'features': [vars(feature) for feature in record.features],
                'protein_existence': record.protein_existence,
                'seqinfo': {k:v for k,v in zip(('length', \
                    'molecular_weight', 'CRC32_value'), record.seqinfo)},
                'sequence': record.sequence,
                'references': self.parse_references(record.references),
                'cross_references': self.parse_cross_references(record.cross_references),
            }
            # self.print_dict(rec)
            yield rec
    
    def parse_references(self, references):
        refs = []
        if references:
            for reference in references:
                ref = {
                        'number': reference.number,
                        'positions': reference.positions,
                        'comments': reference.comments,
                        'authors': reference.authors,
                        'title': reference.title,
                        'location': reference.location,
                }
                for r in reference.references:
                    ref[r[0]] = r[1]
                refs.append(ref)
        return refs

    def parse_cross_references(self, cross_references):
        refs = {}
        if cross_references:
            for items in cross_references:
                Utils.init_dict(refs, [items[0],], [])
                refs[items[0]].append({
                    'id': items[1],
                    'other': list(items[2:]),
                })
        return refs

    def map_term(self, key1:list, key2:list, outfile:str):
        '''
        map swissprot accession number to 
        '''
        map = {}
        handle = self.parse_protein()
        for rec in handle:
            val1 = Utils.get_deep_value(rec, key1)
            val2 = Utils.get_deep_value(rec, key2)
            # print(val1, val2)
            if val1 and val2:
                for k in val1:
                    map[k] = val2
        if outfile and os.path.isdir(os.path.dirname(outfile)):
            File(outfile).save_json(map)
        return map

