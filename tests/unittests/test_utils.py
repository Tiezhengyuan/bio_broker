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
    
    @data(
        [{}, 'a', 1, {'a':[1,]}],
        [{}, 'a', {'b':1}, {'a':[{'b':1},]}],
        [{}, '', 1, {}],
        [{}, '-', 1, {}],
        [{}, None, 1, {}],
        [{'a':[]}, 'a', 1, {'a':[1,]}],
        [{'a':[1,]}, 'a', 1, {'a':[1,]}],
        [{'a':[0,]}, 'a', 1, {'a':[0,1,]}],
        [{'a':[1,]}, 'b', 2, {'a':[1,],'b':[2,]}],
        # val is list
        [{}, 'a', [1,2], {'a':[1,2]}],
        [{'a':[1]}, 'a', [1,2], {'a':[1,2]}],
    )
    @unpack
    def test_update_dict(self, input, key, val, expect):
        Utils.update_dict(input, key, val)
        assert input == expect
    
    @data(
        [{'a':3}, ['a'], [3]],
        [{'a':{'b':{'c':3}}}, ['a', 'b', 'c'], [3]],
        [{'a':{'b':{'c':{'d':[1,2]}}}}, ['a', 'b', 'c'], [{'d':[1,2]}]],
        [[{'a':3},{'a':4}], ['a'], [3,4]],
        [{'b':[{'a':3},{'a':4},{'c':5}]}, ['b','a'], [3,4]],
        [{'b':[{'a':3},{'a':[4]},{'c':5}]}, ['b','a'], [3,4]],
        [{'b':[{'a':3},{'a':4},{'c':5}]}, ['a','b'], []],
        [{'b':[{'a':3},{'a':4},{'c':5}]}, [], []],
    )
    @unpack
    def test_get_deep_value(self, input, keys, expect):
        res = Utils.get_deep_value(input, keys)
        assert res == expect
