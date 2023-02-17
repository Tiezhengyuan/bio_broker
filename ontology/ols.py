"""
source data https://www.ebi.ac.uk/ols/docs/api
"""
import json
from connector.http import HTTP

class OntologyLookupService:
    cache = {}

    def __init__(self):
        endpoint = 'https://www.ebi.ac.uk/ols/api/'
        self.http = HTTP(endpoint)

    def get_ontologies(self):
        self.cache = self.get_ontology_list()
        for ontology_id in self.cache:
            o = self.cache[ontology_id]
            o['terms'] = self.get_ontology_terms(ontology_id, 'terms')
            o['properties'] = self.get_ontology_terms(ontology_id, 'properties')
            o['individuals'] = self.get_ontology_terms(ontology_id, 'individuals')

    def get_ontology_list(self)->dict:
        res = self.http.retrieve_json('ontologies/', {'page':0, 'size':500})
        ontologies = res.get('_embedded', {}).get('ontologies', [])
        ontologies = {i['ontologyId']:i for i in ontologies}
        # print(ontologies)
        return ontologies

    def get_ontology_link(self, ontology_id:str, link_name:str)->dict:
        res = self.http.retrieve_json(f"ontologies/{ontology_id}/{link_name}")
        sub_res = res.get('_embedded', {}).get(link_name, [])
        return sub_res

