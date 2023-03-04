'''
Test class 
'''
from tests.helper import *
from Bio import SeqIO, Seq, SeqRecord
from biofiles.fasta import FASTA


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

    @data(
        ['dna.fa', '1'],
    )
    @unpack
    def test_fasta_to_dict(self, input, expect_id):
        infile = os.path.join(DIR_DATA, input)
        res = FASTA(infile).fasta_to_dict()
        assert expect_id in res