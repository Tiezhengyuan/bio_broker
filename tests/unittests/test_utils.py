'''
Test class 
'''
from unittest import TestCase, mock, skip
from ddt import ddt, data, unpack
import os, sys

from utils.utils import Utils

@ddt
class Test_(TestCase):

    def setUp(self):
        pass

    @skip
    @data(
        [
            ['chrY', 'chr8', 'chrX', 'chr2', 'chr1', 'chr10'],
            ['chr1', 'chr2', 'chr8', 'chr10', 'chrX', 'chrY'],
        ],
    )
    @unpack
    def test_sort_array(self, input, expect):
        res = Utils.sort_array(input)
        assert res == expect


    @data(
        [{}, ['a',], {}, {'a':{}}],
        [{}, ['a',], None, {'a':''}],
        [{'a':[]}, ['a',], {}, {'a':[]}],
        [{}, ['a','b','c'], [], {'a':{'b':{'c':[]}}}],
    )
    @unpack
    def test_init_dict(self, input, keys, default_val, expect):
        Utils.init_dict(input, keys, default_val)
        assert input == expect