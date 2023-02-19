'''
Test class 
'''
from unittest import TestCase, mock
from ddt import ddt, data, unpack
import os, sys

from utils.utils import Utils

@ddt
class Test_(TestCase):

    def setUp(self):
        pass

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