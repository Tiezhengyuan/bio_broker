"""
http://geneontology.org/docs/ontology-documentation/
"""
import json
from connector.http import HTTP


class GeneOntology:
    cache = {}

    def __init__(self):
        endpoint = "http://api.geneontology.org/api/"
        self.http = HTTP(endpoint)

    def get_term(self, term_id:str):
        if not term_id:
            return {}
        # read cache firstly
        if term_id in self.cache:
            return self.cache[term_id]
        # retrieve from HTTP
        term = {
            'id': term_id,
            'bioentity': self.get_bioentity(term_id),
            'topology_graph': self.get_topology_graph(term_id),
        }
        if term['bioentity']:
            self.cache[term_id] = term
        return term
        

    def get_bioentity(self, term_id:str)->dict:
        '''
        return basic info on any bioentity
        '''
        # url =f"http://api.geneontology.org/api/bioentity/function/{term_id}"
        # url =f"http://api.geneontology.org/api/bioentity/{term_id}"
        return self.http.retrieve_json(f"bioentity/{term_id}")

    def get_topology_graph(self, term_id:str)->dict:
        return self.http.retrieve_json(f"ontology/term/{term_id}/graph")

    def retrieve_relations(self, term:dict, relation:str=None)->tuple:
        """
        relation: is_a, part of, regulates, 
            positively regulates, negatively regulates
        """
        parents, children = [], []
        if not relation: relation = 'all'
        topology_graph = term.get("topology_graph_json")
        term_id = term.get('id')
        if term_id and topology_graph:
            for edge in topology_graph.get('edges', []):
                if relation == edge['pred'] or relation == 'all':
                    if term_id == edge['sub']:
                        parents.append(edge['obj'])
                    elif term_id == edge['obj']:
                        children.append(edge['sub'])
        return parents, children

