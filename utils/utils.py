"""

"""

import gzip
import os, sys
import re
import json

class Utils:

    @staticmethod
    def sort_array(arr):
        '''
        element: characters+numerics
        for example: sort chromosome name
        '''
        arr_len = len(arr)
        for i in range(0, arr_len-1):
            for j in range(1, arr_len):
                a=arr[j-1][3:]
                a_char= re.findall(r"[^0-9]", a)
                b=arr[j][3:]
                b_char= re.findall(r"[^0-9]", b)
                #a is char
                if a_char:
                    if b_char==[] or (b_char and a>b):
                        arr[j], arr[j-1] = arr[j-1], arr[j]
                #a_char==[]
                else:
                    if b_char==[] and int(a)>int(b):
                        arr[j], arr[j-1] = arr[j-1], arr[j]
        return arr
    
    @staticmethod
    def init_dict(input:dict, keys:list, default_val=None):
        '''
        arg: default_val = '', [], {}
        '''
        curr = input
        if isinstance(input, dict):
            for k in keys[:-1]:
                if k not in curr:
                    curr[k] = {}
                curr = curr[k]
            if keys[-1] not in curr:
                curr[keys[-1]] = default_val if \
                    default_val is not None else ''


    @staticmethod
    def update_dict(input:dict, key, val):
        if key not in ('', '-', None):
            if key in input:
                if isinstance(input[key], list) \
                    and val not in input[key]:
                    input[key].append(val)
            else:
                input[key] = [val,]

