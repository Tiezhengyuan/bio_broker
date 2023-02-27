'''
Test class 
'''
from unittest import TestCase, mock, skip
from ddt import ddt, data, unpack
import os
from copy import deepcopy
from utils.jtxt import Jtxt

env = {
    'DIR_CACHE': "H:\\cache",
    'DIR_DOWNLOAD': "H:\\download",
}
dir_data = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

@ddt
class TestJtxt(TestCase):
    jtxt_file = os.path.join(dir_data, 'test_jtxt.jtxt')

    @mock.patch.dict(os.environ, env)
    def setUp(self):
        self.c = Jtxt(self.jtxt_file)

    @mock.patch.dict(os.environ, env)
    def tearDown(self):
        if os.path.isfile(self.jtxt_file):
            os.remove(self.jtxt_file)

    # @skip
    @data(
        [{}, True, {}],
        [
            {'a':1, 'b':[1,2], 'c':[{'a':1},{'a':2},], 'd':'', 'e':None},
            True,
            {'a':1, 'b':[1,2], 'c':[{'a':1},{'a':2},], 'd':'', 'e':None},
        ],
        [
            {'a':1, 'b':[1,2], 'c':[{'a':1},{'a':2},], 'd':'', 'e':None},
            None,
            {'a':1}
        ],
    )
    @unpack
    def test_handle_jtxt(self, input, is_oneline, expect):
        self.c.save_jtxt(input, is_oneline)
        handle = self.c.read_jtxt(True)
        res = next(handle)
        assert res == expect

    # @skip
    @data(
        [ ['a',], [[1]] ],
        [ ['b',], [[1,2]] ],
        [ ['c','a'], [[1,2]] ],
        [ ['d',], []],
        [ ['e',], []],
        # alternative cases
        [ [], []],
        [ ['wrong'], []],
        [ ['c', 'wrong'], []],
    )
    @unpack
    def test_search_jtxt(self, keys, expect):
        data = {
            'a':1,
            'b':[1,2],
            'c':[{'a':1},{'a':2},{'d':3},],
            'd':'',
            'e':None,
        }
        self.c.save_jtxt(data, True)
        res = self.c.search_jtxt(keys)
        assert res == expect


    def test_append_jtxt(self):
        # one line
        self.c.save_jtxt({'a':0})

        # two lines
        self.c.append_jtxt({'a':1})
        handle = self.c.read_jtxt(True)
        res = next(handle)
        assert res == {'a':0}
        assert len(list(handle)) == 1

        # three lines
        self.c.append_jtxt({'b':2})
        handle = self.c.read_jtxt(True)
        assert len(list(handle)) == 3
