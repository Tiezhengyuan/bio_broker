'''
Test class 
'''
from tests.helper import *
from annotation.map_protein import MapProtein


@ddt
class TestMapProtein(TestCase):

    @mock.patch.dict(os.environ, env)
    def setUp(self):
        self.c = MapProtein()

    
    @mock.patch.dict(os.environ, env)
    def test_process(self):
        self.c.process()
