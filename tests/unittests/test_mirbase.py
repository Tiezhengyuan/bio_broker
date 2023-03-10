'''
Test class 
'''
from tests.helper import *
from database.mirbase import miRBase


class Test_(TestCase):
    

    def setUp(self):
        pass

    @skip
    @mock.patch.dict(os.environ, env)
    def test_download_hairpin(self):
        miRBase().download_hairpin()

    @skip
    @mock.patch.dict(os.environ, env)
    def test_download_mature(self):
        miRBase().download_mature()
    

    def test_filter_seq_records(self):
        fa_file = os.path.join(env['DIR_DOWNLOAD'], 'hairpin.fa.gz')
        res = miRBase().filter_seq_records(fa_file, "Homo sapiens")
        assert len(list(res)) > 0
        # for i in res:
        #     print(i)

    @mock.patch.dict(os.environ, env)
    def test_prepare_selected_mirseq(self):
        fa_file = os.path.join(env['DIR_DOWNLOAD'], 'hairpin.fa.gz')
        miRBase().prepare_selected_mirseq(fa_file, "Homo sapiens")
