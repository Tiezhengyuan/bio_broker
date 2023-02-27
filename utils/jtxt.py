"""
bio-broker define a customary format file that combines json and text
jtxt format could hanlde huge data up to ~GB due RAM limits
"""
from typing import Iterable
import json
from utils.utils import Utils
from utils.commons import Commons

class Jtxt(Commons):
    def __init__(self, file:str):
        super(Jtxt, self).__init__()
        self.file = file

    def save_jtxt(self, input:dict, is_oneline:bool=None):
        if not isinstance(input, dict):
            return False
        if is_oneline is None:
            is_oneline = False
        with open(self.file, 'w') as f:
            if is_oneline:
                line = json.dumps(input)
                f.write(line)
            else:
                for k in input:
                    rec = {k: input[k]}
                    line = json.dumps(rec) + '\n'
                    f.write(line)
        return True

    def read_jtxt(self, yield_dict:bool=False)->Iterable:
        with open(self.file, 'rt') as f:
            for line in f:
                records = json.loads(line)
                if yield_dict:
                    yield records
                else:
                    for k,v in records.items():
                        yield (k,v)

    def append_jtxt(self, input:dict):
        with open(self.file, 'a+') as f:
            line = json.dumps(input)
            f.write(line+'\n')
            # print(f"Append data into {self.file}")
        return True
    
    def search_jtxt(self, keys:list):
        if not keys: return []
        res = []
        handle = self.read_jtxt(True)
        for record in handle:
            val = Utils.get_deep_value(record, keys)
            if val not in (res, None, [], {}):
                res.append(val)
        return res
