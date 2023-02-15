# bio_broker
This bioinformatic library offers toolts that could retrieve, download, and integrate data from bioinformatics databases.

# 1. Objectives

## Functionality:
- Download reference genome from NCBI, EBI, etc.
- Retrieve sequences based on certain references namely accession number.
- Retrieve and integrate ontology terminology.
- Integrate genome annotations.

## Target users:
- Developers who may borrow some source code for their development.
- Bioinformaticians who may wrap bio-broker and develop their pipelines.
- Data engineers who may apply bio-broker to integrate bioinformatics data and develop databases.
- Biologists who want to compare their own data with public data and perform association analysis.


# 2. installation
Bio-broker is developed and tested under Python 3.8.

>pip install -r requirements.txt

# 3. Tests


## 3.1. Unit testing

> pytest tests/unittests

## 3.2. local testing

> pytest tests/localtests


# references
TCGA: https://docs.cancergenomicscloud.org/docs/tcga-data
