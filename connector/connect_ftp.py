"""
connect FTP
"""
import os
import time
from typing import Callable
from ftplib import FTP
from utils.dir import Dir

class ConnectFTP:
    def __init__(self, endpoint:str, username:str=None, password:str=None):
        self.endpoint = endpoint
        self.ftp = FTP(self.endpoint)
        if username or password:
            self.ftp.login(username, password)
        else:
            self.ftp.login()
        self.dir_download = os.environ.get('DIR_DOWNLOAD', '')

    def is_dir(self, name=str):
        origin_dir = self.ftp.pwd()
        try:
            self.ftp.cwd(name)
            self.ftp.cwd(origin_dir)
            return True
        except Exception as e:
            # print(e)
            pass
        # print('origin dir: ', self.ftp.pwd())
        return False
    


    def download_file(self, ftp_path:str, file_name:str, local_path:str=None):
        origin_ftp_path = self.ftp.pwd()
        if ftp_path:
            self.ftp.cwd(ftp_path)
        if local_path is None:
            local_path = self.dir_download
        local_file = os.path.join(local_path, file_name)
        try:
            with open(local_file, 'wb') as f:
                self.ftp.retrbinary(f"RETR {file_name}", f.write)
                print(f"Download data from {self.ftp.pwd()} into {local_file}.")
        except Exception as e:
            # print('Failure: download data from FTP', file)
            os.remove(local_file)
            return False
        # go back
        self.ftp.cwd(origin_ftp_path)
        return True

    def download_files(self, ftp_path:str=None, \
            file_pattern:str=None, local_path:str=None):
        local_files = []
        if local_path is None:
            local_path = self.dir_download
        origin_ftp_path = self.ftp.pwd()
        if ftp_path:
            self.ftp.cwd(ftp_path)
        for file in self.ftp.nlst():
            if not self.is_dir(file):
                if file_pattern is None or file.endswith(file_pattern):
                    local_file = os.path.join(local_path, file)
                    try:
                        with open(local_file, 'wb') as f:
                            self.ftp.retrbinary(f"RETR {file}", f.write)
                        local_files.append(local_file)
                        print(f"Download data from {self.ftp.pwd()} as {local_file}")
                    except Exception as e:
                        # print('Failure: download data from FTP', file)
                        pass
        # go back
        self.ftp.cwd(origin_ftp_path)
        return local_files

    def download_tree(self, local_name:str, ftp_path:str=None,\
            file_pattern:str=None):
        '''
        arg: local_name is determined by os.path.join()
        Download FTP directory recursively
        '''
        #initialize local_path
        local_path = os.path.join(self.dir_download, local_name)
        Dir(local_path).init_dir()
        # initialize ftp_path
        origin_ftp_path = self.ftp.pwd()

        # scan ftp path
        local_files = []
        pool = [(ftp_path, local_path)]
        while pool:
            self.ftp.cwd(origin_ftp_path)
            _ftp_path, _local_path = pool.pop(0)
            if _ftp_path:
                self.ftp.cwd(_ftp_path)
            print(self.ftp.pwd(), self.ftp.nlst())
            # check if name is directory
            for name in self.ftp.nlst():
                if self.is_dir(name):
                    sub_ftp_path = f"{_ftp_path}/{name}"
                    sub_local_path = os.path.join(_local_path, name)
                    Dir(sub_local_path).init_dir()
                    pool.append((sub_ftp_path, sub_local_path))
            #download files
            local_files += self.download_files(
                None, file_pattern, _local_path)
        return local_files

