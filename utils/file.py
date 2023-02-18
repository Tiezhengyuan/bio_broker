import os, sys
import re

class File:
    def __init__(self, infile):
        self.infile = infile

    def readonly_handle(self):
        '''
        ouput is read-only file handle
        '''
        if infile.endswith('.gz'):
            in_obj = gzip.open(self.infile, 'rt')
        else:
            in_obj = open(self.infile, 'rt')
        return in_obj




    def list_to_file(self, inlist, out_file):
        '''
        export list to a text file seperated by return
        '''
        out_obj = open(out_file, 'wt')
        for key in inlist:
            out_obj.write(str(key)+'\n')
        out_obj.close()
        print('write a list to ', out_file)

    def file_to_list(self):
        '''
        read certain column in a file
        '''
        outlist=[]
        try: 
            in_obj = self.readonly_handle(self.infile)
            for line in in_obj:
                line = line.strip()
                outlist.append(line)
            in_obj.close()
        except FileNotFoundError:
            print(self.infile, 'didnot exit!')
            pass
        return outlist

    def file_to_dict(self, pattern=","):
        outdict={}
        IN=open(self.infile, 'r')
        for line in IN:
            line = line.rstrip()
            if line.startswith('#'):
                continue
            else:
                items=line.split(pattern)
                outdirct[items[0]]=items[1]
        IN.close()
        return outdirct
