'''
Map Entrez Gene 
'''
import os
import json
from utils.commons import Commons
from utils.file import File
from utils.dir import Dir
from utils.utils import Utils
from annotation.map import Map

class MapGene(Map):

    def __init__(self):
        super(MapGene, self).__init__()
    
    def process(self, tax_id:str):
        # geneid ~ ...
        self.get_map(f"{tax_id}_gene2accession.json", 'Symbol')
        self.get_map(f"{tax_id}_gene_info.json", 'chromosome')
        self.get_map(f"{tax_id}_gene2accession.json", \
            'start_position_on_the_genomic_accession')

        # within record
        self.get_intra_map(f"{tax_id}_gene2ensembl.json", \
            "Ensembl_gene_identifier", "GeneID")
        self.get_intra_map(f"{tax_id}_gene2ensembl.json", \
            "Ensembl_protein_identifier", "GeneID")
        self.get_intra_map(f"{tax_id}_gene2ensembl.json", \
            "Ensembl_rna_identifier", "GeneID")

    def geneid_to_symbol(self, tax_id:str):
        '''
        geneid ~ gene symbols
        '''
        return self.get_map(f"{tax_id}_gene2accession.json", 'Symbol')

    def geneid_to_chromosome(self, tax_id:str):
        '''
        geneid ~ chromosomes
        '''
        return self.get_map(f"{tax_id}_gene_info.json", 'chromosome')

    def geneid_to_start_position(self, tax_id:str):
        '''
        geneid ~ start position on chromosome
        '''
        return self.get_map(f"{tax_id}_gene2accession.json", \
                    'start_position_on_the_genomic_accession')

    def ensembl_geneacc_to_geneid(self, tax_id:str):
        '''
        Ensembl accession ENSG... ~ geneid
        '''
        return self.get_intra_map(f"{tax_id}_gene2ensembl.json", \
                        "Ensembl_gene_identifier", "GeneID")

    def ensembl_proacc_to_geneid(self, tax_id:str):
        '''
        Ensembl protein accession ENSP... ~ geneid
        '''
        return self.get_intra_map(f"{tax_id}_gene2ensembl.json", \
                        "Ensembl_protein_identifier", "GeneID")

    def ensembl_rnaacc_to_geneid(self, tax_id:str):
        '''
        Ensembl transcript accession ENSP... ~ geneid
        '''
        return self.get_intra_map(f"{tax_id}_gene2ensembl.json", \
                        "Ensembl_rna_identifier", "GeneID")
    

