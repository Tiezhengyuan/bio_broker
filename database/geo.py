"""
Gene Expression Omnibus: a data repository of 
high-throughput gene expression and hybridization array data. 
""" 
import os, sys, re
from bs4 import BeautifulSoup
from Bio import Entrez, Geo
import pandas as pd

from connector.http import HTTP
from connector.connect_ftp import ConnectFTP
from utils.threading import Threading
from utils.file import File
from database.ncbi_entrez import NCBIEntrez

class GEO(NCBIEntrez):
    db = 'gds'

    def __init__(self):
        super(GEO, self).__init__()
        self.ftp_endpoint = 'ftp.ncbi.nlm.nih.gov'
        self.dir_download = os.environ.get('DIR_DOWNLOAD')

    def retrieve_uids(self, term:str):
        '''
        get uids by GEO accession number
        those uids define: platform GPL..., sample GSM..., series GSE...
        retrieve 20 UID per time
        '''
        res = self.search_entrez(db=self.db, term=term)
        ids = sum(res, [])
        ids = sorted(list(set(ids)), key=int)
        return ids
    

    def retrieve_summary(self, id_list:list)->dict:
        '''
        all ids comes from one GSE 
        series GSE, platform: GPL, sample GSM
        '''
        geo = {'samples':[]}
        for id in id_list:
            rec = self.efetch(db=self.db, id=id)
            # print(repr(rec))
            # print(rec)
            acc = self.parse_accession(rec)
            if acc.startswith('GPL'):
                geo['platform'] = {
                    'uid': id,
                    'accession': acc,
                    'title': self.parse_title(rec),
                    'desc': self.parse_desc(rec),
                    'ftp_url': self.parse_ftp_url(rec),
                }
            elif  acc.startswith('GSE'):
                geo['organism'] = self.parse_organism(rec)
                geo['type'] = self.parse_type(rec)
                geo['series'] = {
                    'uid': id, 
                    'accession': acc,
                    'title': self.parse_title(rec),
                    'desc': self.parse_desc(rec),
                    'ftp_url': self.parse_ftp_url(rec),
                }
            else:
                geo['samples'].append({
                    'uid': id, 
                    'accession': acc,
                    'title': self.parse_title(rec),
                    'source_name': self.parse_source_name(rec),
                })
        return geo

    def parse_accession(self, rec:str):
        return ','.join(re.findall(r'Accession:[\t+|\s+](\w*)', rec))
    def parse_title(self, rec:str):
        return ','.join(re.findall(r'\n1.[\s+|\t+](.*)\n', rec))
    def parse_desc(self, rec:str):
        return ' '.join(re.findall(r'\(Submitter supplied\) (.*)', rec))
    def parse_organism(self, rec:str):
        return ','.join(re.findall(r'Organism:\t+(.*)', rec))
    def parse_type(self, rec:str):
        return ','.join(re.findall(r'Type:\t+(.*)', rec))
    def parse_platform(self, rec:str):
        return ','.join(re.findall(r'Platform:[\t+|\s+](.*)', rec))
    def parse_ftp_url(self, rec:str):
        return ','.join(re.findall(r'ftp://(.*)', rec))
    def parse_source_name(self, rec:str):
        return ','.join(re.findall(r'Source name:\s+(.*)', rec))
    def parse_samples(self, rec:str):
        return ','.join(re.findall(r'Series[\t+|\s+](\w*)', rec))

    def retrieve_geo_ftp_url(self, id_list:list):
        for id in id_list:
            rec = self.efetch(db=self.db, id=id)
            acc = self.parse_accession(rec)
            print(acc)
            if  acc.startswith('GSE'):
                print(rec)
                return self.parse_ftp_url(rec)

    def download_data(self, GSE:str):
        # get FTP path
        ids = self.retrieve_uids(GSE)
        ftp_url = self.retrieve_geo_ftp_url(ids)
        # print(ftp_url)

        # download data from FTP
        ftp_path = ftp_url.replace(self.ftp_endpoint, '')
        ConnectFTP(self.ftp_endpoint).download_tree(
            GSE, ftp_path, None)


    def read_data(self, GSE:str):
        matrix_path = os.path.join(self.dir_download, GSE, 'matrix', \
            f"{GSE}_series_matrix.txt.gz")
        metadata, data = {}, {}
        with File(matrix_path).readonly_handle() as f:
            for line in f:
                line = line.rstrip()
                if line.startswith('!'):
                    line = line.replace("\"", "").rstrip()
                    items = line[1:].split('\t')
                    # print(items)
                    if len(items) == 2:
                        if 'Series_sample_id' == items[0]:
                            # print(repr(line))
                            data[items[0]] = items[1].split(' ')
                        else:
                            metadata[items[0]] = items[1]
                    elif len(items) > 2:
                        data[items[0]] = items[1:]
        #convert data to data frame
        d = pd.DataFrame.from_dict(data, orient='index')
        d.columns = data['Sample_title']
        # print(d)
        # print(metadata)

        # read suppl_counts
        counts = None
        if 'Series_supplementary_file' in metadata:
            filename = os.path.basename(metadata['Series_supplementary_file'])
            local_path = os.path.join(self.dir_download, GSE, 'suppl', filename)
            print(local_path)
            counts = pd.read_csv(local_path, sep=',', header=0, index_col=0)
            # print(counts)
            # print(counts.shape)
        return  metadata, data, counts

    # def read_suppl_counts(self, filename):
        # for k,v in data.items():
        #     print(k, len(v), v)

