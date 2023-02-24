"""
KEGG: 
"""
import os
from connector.connect_ftp import ConnectFTP


class KEGG(ConnectFTP):
    def __init__(self, endpoint:str=None):
        if endpoint is None:
            endpoint = 'ftp.genome.jp'
        super(KEGG, self).__init__(endpoint)
        self.dir_local = os.path.join(self.dir_download, "kegg")
    
    def download_data(self):
        '''
        download KEGG data including subdirectories and files
        '''
        local_files = self.download_tree(
            local_name = 'kegg',
            ftp_path = 'pub/kegg'
        )
        return local_files
