'''
Test class 
'''
from unittest import TestCase, mock, skip
from ddt import ddt, data, unpack
import os

from annotation.map_cache import MapCache

env = {
    'DIR_CACHE': "H:\\cache",
    'DIR_DOWNLOAD': "H:\\download",
}


@ddt
class TestMap(TestCase):

    @data(
        [
            ["taxonomy", '9606', "GeneID", "Ensembl",],
            ["H:\\cache\\map\\96\\06\\GeneID_Ensembl.json"],
        ],
        [['wrong'], None],
        [["taxonomy", 'wrong'], []],
    )
    @unpack
    @mock.patch.dict(os.environ, env)
    def test_get_map_path(self, keys, expect):
        res = MapCache(keys).get_map_path()
        assert res == expect