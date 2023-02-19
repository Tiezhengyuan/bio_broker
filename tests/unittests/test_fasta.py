'''
Test class 
'''
from unittest import TestCase, mock
from ddt import ddt, data, unpack
import os, sys
from Bio import SeqIO, Seq, SeqRecord

from biofiles.fasta import FASTA

DIR_CACHE = "F:\\bio_broker\\cache"
DIR_DOWNLOAD = "F:\\bio_broker\\download"
DIR_DATA = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')


@ddt
class Test_(TestCase):

    def setUp(self):
        pass

    @data(
        ['dna.fa', '1', 'ATCG'],
        ['dna.fa.gz', '1', 'ATCG'],
        ['wrong.fa', None, None],
    )
    @unpack
    def test_read_handler(self, input, expect_id, expect_seq):
        infile = os.path.join(DIR_DATA, input)
        res = FASTA(infile).read_handler()
        if res:
            for seq in res:
                assert seq.id == expect_id
                assert seq.seq == expect_seq
                break
    
    def test_write_handler(self):
        sequences = iter([SeqRecord.SeqRecord(Seq.Seq('ATCG'), id='1'),])
        outfile = os.path.join(DIR_DATA, 'wirte_fasta.fa')
        FASTA(outfile).write_handler(sequences)