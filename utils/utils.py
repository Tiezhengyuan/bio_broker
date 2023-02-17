"""

"""

import gzip
import os, sys
import re
import json

class Utils:
    def __init__(self):
        pass
    
    @staticmethod
    def print_dict(self, indict):
        '''
        print dictionary to stdout for debugging
        '''
        n = 1
        for key in sorted(indict.keys()):
            print('{:5}: {:10}\t{}'.format(n, key, indict[key]))
            n += 1

        


    



