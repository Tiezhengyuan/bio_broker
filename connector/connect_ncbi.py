"""
download data from NCIB FTP
"""
import os
from connector.connect_ftp import ConnectFTP

class ConnectNCBI(ConnectFTP):
    def __init__(self, endpoint:str=None):
        if endpoint is None:
            endpoint = 'ftp.ncbi.nlm.nih.gov'
        super(ConnectNCBI, self).__init__(endpoint)
        self.dir_local_ncbi = os.path.join(self.dir_download, "NCBI")
    
    def download_gene_data(self):
        '''
        download gene/DATA including subdirectories and files
        '''
        local_files = self.download_tree(
            local_name = os.path.join('NCBI', 'gene', 'DATA'),
            ftp_path = 'gene/DATA',
            file_pattern = '.gz'
        )
        return local_files
