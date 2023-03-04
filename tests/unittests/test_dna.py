'''
Test class 
'''
from tests.helper import *
from sequence.dna import DNA

@ddt
class Test_(TestCase):

    def setUp(self):
        pass

    def test_(self):
        DNA('ATGC')
    
    def test_count_subseq(self):
        res = DNA('ATGATCTA').count('AT')
        assert res == 2

    def test_locate_subseq(self):
        res = DNA('GATCTA').find('AT')
        assert res == 1

    def test_complement(self):
        res = DNA('GATCTA').complement()
        assert res == 'CTAGAT'

    def test_reverse_complement(self):
        res = DNA('GATCTA').reverse_complement()
        assert res == 'TAGATC'

    @data(
        ['GATCTA', 'DL'],
        ["ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG", 'MAIVMGR*KGAR*'],
        # ['AT', ''],
    )
    @unpack
    def test_to_protein(self, seq, expect):
        res = DNA(seq).translate()
        assert res == expect

    def test_to_rna(self):
        res = DNA('GATCTA').transcribe()
        assert res == 'GAUCUA'
    
    @data(
        ['GATCTCTAG', True],
        ['GATCCTAG', True],
        ['GAG', True],
        ['GG', True],
        ['GATT', False],
        ['', False],
    )
    @unpack
    def test_is_palindromic(self, input, expect):
        res = DNA.is_palindromic(input)
        assert res == expect
