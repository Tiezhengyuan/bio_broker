# bioBroker
bioBroker is a bioinformatic library offers tremendous classes and methods
that could retrieve, download, and integrate various data.
Those classes or methods could be middleware of other bioinformatics applications.

# 1. Introduction

## Functionality
- Download reference genome from NCBI, EBI, etc.
- Retrieve sequences based on certain references namely accession number.
- Retrieve and integrate ontology terminology.
- Integrate genome annotations.

## Target users
- Developers who may borrow some source code for their development.
- Bioinformaticians who may wrap bio-broker and develop their pipelines.
- Data engineers who may apply bio-broker to integrate bioinformatics data and develop databases.
- Biologists who want to compare their own data with public data and perform association analysis.

## Recommendations
- bioBroker could work as middle layer for a bioinformatics web service,
  or integrated into a certain bioinformatics pipelines.
- bio-broker could integrate various source of biomedical data and serve
  design of new databases.
- Bioinformatics developer is recommended to keep consistency between requirements
  and source coding work.


# 2. installation

## install bio-broker
bioBroker is developed and tested under Python 3.8. Steps of installation is described as the below:

```
git clone git@github.com:Tiezhengyuan/bio_broker.git
cd bio_broker
pip install -r requirements.txt
```

## install Redis
Run the following command from the shell. The docker should be run at host=127.0.0.1, port=6379.
```
docker pull redis
docker run -it --rm --name redis -p 6379:6379 redis
```


# 3. Tests

Design and Devlopment of bio-broker follows process of Test-Driven Development(TDD).
In this process, all needs are elicited into requirements, and converted into source code.
Most source code should be covered by unit tests and local tests with >80% coverage.

## 3.1. Unit testing
Unit testing include many testing cases that test functionality of single class or method.

```
pytest tests/unittests
```

## 3.2. Local testing
For local testing, testing cases make sure that a certain function is working.

```
pytest tests/localtests
```

# references
## Ontology
THE CANCER GENOME ATLAS (TCGA) PROJECT: https://docs.cancergenomicscloud.org/docs/tcga-data
Gene Ontology: http://geneontology.org/docs/ontology-documentation/
API of GO: http://api.geneontology.org/api
Disease Ontology: https://www.disease-ontology.org/
Ontology Looup Service (OLS): https://www.ebi.ac.uk/ols/index/
NCBI-Entrez:  https://eutils.ncbi.nlm.nih.gov