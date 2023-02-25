"""

"""
from copy import deepcopy
import gzip
import os, sys
import re

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

    @staticmethod
    def get_deep_value(input:dict, keys:list):
        if not keys:
            return []
        val = []
        pool = [(keys, input),]
        while pool:
            curr_keys, curr_input = pool.pop(0)
            # print(curr_keys, curr_input)
            if isinstance(curr_input, dict):
                key = curr_keys[0]
                if key in curr_input:
                    if len(curr_keys) == 1:
                        tmp = []
                        if isinstance(curr_input[key], list):
                            tmp += curr_input[key]
                        else:
                            tmp = [curr_input[key]]
                        for t in tmp:
                            if t not in val:
                                val.append(t)
                    else:
                        pool.append((curr_keys[1:], curr_input[key]))
            elif isinstance(curr_input, list):
                for item in curr_input:
                    pool.append((curr_keys, item))
        return val
    
    @staticmethod
    def merge_dict(d1:dict, d2:dict)->dict:
        '''
        values of corresponding keys between d1 and d2
        should match to each other
        '''
        # d = deepcopy(d1)
        pass