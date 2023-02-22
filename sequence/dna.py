"""
DNA sequence
"""
from Bio.Seq import Seq

class DNA(Seq):
    def __init__(self, seq:str=None, len:int=None):
        super(DNA, self).__init__(seq, len)
    
    @staticmethod
    def is_palindromic(seq:str, iter:str=None):
        if iter is None: iter = 0
        if len(seq) >= 2:
            first, last = seq[0], seq[-1]
            if first == last:
                return DNA.is_palindromic(seq[1:-1], iter+1)
            return False
        else:
            if iter == 0:
                return False
        return True
    
    def locate_subseq(self, sub_str:str):
        '''
        index 0-...
        '''
        return self.seq.find(sub_str)