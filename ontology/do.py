"""
source data https://github.com/DiseaseOntology/HumanDiseaseOntology
"""
import json
import obonet

class DiseaseOntology:
    def __init__(self):
        self.endpoint = 'https://raw.githubusercontent.com/DiseaseOntology/'
    
    def get_doid(self)->dict:
        url = f"{self.endpoint}HumanDiseaseOntology/main/src/ontology/doid.obo"
        graph = obonet.read_obo(url)
        hdo = { id_:data for id_, data in graph.nodes(data=True)}
        return hdo
