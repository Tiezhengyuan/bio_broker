
import os
import xml.dom.minidom

class Commons:
    cascade_num = 2
    
    def __init__(self):
        self.dir_download = os.environ.get('DIR_DOWNLOAD', '')
        self.dir_cache = os.environ.get('DIR_CACHE', '')
        self.dir_bin = os.environ.get('DIR_BIN', '')
    
    def print_xml(self, xml_str:str):
        temp = xml.dom.minidom.parseString(xml_str)
        new_xml = temp.toprettyxml()
        print(new_xml)
    
    def print_dict(self, indict):
        '''
        print dictionary to stdout for debugging
        '''
        n = 1
        for key in sorted(indict.keys()):
            print('{:5}: {:10}\t{}'.format(n, key, indict[key]))
            n += 1
