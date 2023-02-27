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

    def parse_protein(self)->Iterable:
        local_file = os.path.join(self.dir_local, 'uniprot_sprot.dat.gz')
        handle = File(local_file).readonly_handle()
        for record in SwissProt.parse(handle):
            rec = {
                'accessions': [{'uniprotkb_acc':acc} for acc in record.accessions],
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
                'protein_sequence': record.sequence,
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
                id_name = 'id'
                if items[0] == 'EMBL':
                    id_name = 'embl_acc'
                elif items[0] == 'GO':
                    id_name = 'go'
                elif items[0] == 'RefSeq':
                    id_name = 'refseq_acc'
                elif items[0] == 'KEGG':
                    id_name = 'kegg_gene'
                refs[items[0]].append({
                    id_name: items[1],
                    'other': list(items[2:]),
                })
        return refs



