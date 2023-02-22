"""
UniGene is an NCBI database of the transcriptome, 
with each UniGene record showing the set of transcripts 
that are associated with a particular gene in a specific organism.
"""

from Bio import UniGene

class UniGene:
    def __init__(self, endpoint):
        self.endpoint = endpoint
    
    