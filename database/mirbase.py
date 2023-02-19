"""
microRNA: mirBase: https://www.mirbase.org/
"""
import argparse
import os
import sys
import re
from Bio import SeqIO

from connector.http import HTTP
from biofiles.fasta import FASTA

class miRBase:
    def __init__(self):
        endpoint = 'https://www.mirbase.org/'
        self.c = HTTP(endpoint)
        self.dir_cache = os.environ.get('DIR_CACHE', '')
        self.dir_download = os.environ.get('DIR_DOWNLOAD', '')


    def download_hairpin(self):
        '''
        Download hairpin.fa
        '''
        local_file = self.c.download_file(
            self.dir_download, 'ftp/CURRENT/hairpin.fa.gz'
        )
        # print(local_file)

    def download_mature(self):
        '''
        Download mature.fa
        '''
        local_file = self.c.download_file(
            self.dir_download, 'ftp/CURRENT/mature.fa.gz'
        )
        print(local_file)
    
    def filter_seq_records(self, fa_file:str, match_pattern:str):
        records = FASTA(fa_file).read_handler()
        for record in records:
            desc = str(record.description)
            if re.search(match_pattern, desc):
                yield record
            

    def prepare_selected_mirseq(self, infile:str, specie:str):
        '''
        arg: mirna could be hairpin, mature
        '''
        prefix = os.path.join(self.dir_cache, os.path.basename(infile).split('.')[0])
        outfile = f"{prefix}_{specie.replace(' ', '_')}.fa"
        with open(outfile, 'w') as f:
            filtered_sequences = self.filter_seq_records(infile, specie)
            SeqIO.write(filtered_sequences, f, "fasta")


