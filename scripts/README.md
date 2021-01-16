# 
 These are the scripts for GA4GH Federated Analysis Systems Project

[TOC]



------

Script summary

![scriptGrid](fasp/runner/credits/images/scriptgrid.png)

## **Prerequisites to run**

- fasp package - install (e.g. pip) from fasp-scripts directory
- Settings file
  - The examples directory contains a template settings file with a number of parameters for the FASP scripts. Place a copy of this file in your file system and set the environment variable FASP_SETTINGS to point to it. Edit the settings as appropriate.
- Python 3
  - See the code for the modules required
- A folder in your home directory called .keys containing keys for various services. Not all  keys required for all scripts.
  - bdc_credentials.json - api_key file [obtained from BioDataCatalyst](https://gen3.biodatacatalyst.nhlbi.nih.gov/identity)
  - crdc_credentials.json - api_key file [obtained from Cancer Research Data Commons](https://nci-crdc.datacommons.io/identity)
  - anvil_credentials.json - api_key file [obtained from Anvil](https://gen3.theanvil.io)
  - sevenbridges_keys.json - keys for cgc and or cavatica
- The following modules are used by different scripts. All scripts are unlikely to be relevant to all users these modules are not installed with the fasp package. Please install those needed for the scripts you will run.
  - Google Life Sciences API enabled for your GCP account
  - BigQuery python libraries - for scripts that use BigQuery
  - Seven Bridges API
  - [pyega3](https://pypi.org/project/pyega3/) - EGA client libraries for download. See also [EGA documentation for client API](https://ega-archive.org/download/downloader-quickguide-APIv3). 

------

## Scripts

#### Thousand Genomes FASP - FASPScript4.py

This script queries Thousand Genomes data on subjects and specimens which was exported from BioDataCatalyst and loaded into BigQuery.

- [FASPScript4](https://github.com/ga4gh/fasp-scripts/blob/master/fasp/scripts/FASPScript4.py) uses the following GA4GH APIs to perform each step
   - Discovery Search Server (DNA Stack) - Presto on BigQuery
   - DRS server (BioDataCatalyst)
   - WES Server (DNA Stack)
fasp-scripts/blob/master/fasp/scripts
The other two scripts were proof of concept using direct APIs from different stacks
 - [FASPScript1](https://github.com/ga4gh/fasp-scripts/blob/master/fasp/scripts/FASPScript1.py) uses BigQuery for the query and directly submits a GCP Life Sciences pipeline for the compute. This compute uses samtools stats.
 - [FASPScript3](https://github.com/ga4gh/fasp-scripts/blob/master/fasp/scripts//FASPScript3.py) is the same as but substitutes in public DNAStack Discovery Search server for search

- Possible to do's

  - Troubleshoot samtools stats workflow on DNAStack WES server 

#### GWAS workflow 

Script: [FASPScriptGWAS.py](https://github.com/ga4gh/fasp-scripts/blob/master/fasp/scripts/FASPScriptGWAS.py)


- Queries Discovery Search for Thousand Genomes non-annotated recalibrated vcf file for Chromosome 21, obtaining prefixed DRS ids for the file. 
- Resolves which DRS server needs to be called to obtain a URL to access the file.
- Submits the GWAS WDL workflow to the DNAStack WES Server using the URL provided by DRS.

#### Demonstration of Search and compute from multiple sources 

Script: [FASPScript2.py](https://github.com/ga4gh/fasp-scripts/blob/master/fasp/scripts//FASPScript2.py)


- Query COPDGene data in BigQuery, exported from BioDataCatalyst via PFB.

- Query TCGA data in the ISB-CGC tables in BigQuery,

- Both queries use an appropriate prefix to identify which DRS server should be called to obtain a url to the file.

  Currently submits directly to a GCP Life Sciences pipeline. This will be substituted by a submission to a WES Server.

  Both datasets are controlled access data. Access is controlled by the respective Fence access tokens on the CRDC and BioDataCatalyst DRS servers. The COPD data in BigQuery is under GCP IAM access control.




- Possible to do's

  - Add additional dbGaP datasets.
  - Move query to Discovery Search - requires access control on Discovery Search.

#### Reproducibility across stacks 

Script: [FASPScript8.py](https://github.com/ga4gh/fasp-scripts/blob/master/fasp/scripts/FASPScript8.py)


- Queries TCGA data via BigQuery to obtain DRS ids
- Uses DRS to identify files for these cases are on both Google Cloud and AWS
- Runs samtools stats on Google Cloud and Seven Bridges (AWS)

#### Compute on SRA (NCBI Sequence Read Archive) urls 

Script: [FASPScript6.py](https://github.com/ga4gh/fasp-scripts/blob/master/fasp/scripts/FASPScript6.py)


- This script demonstrates that the DNAStack WES Server can perform a compute on the urls returned by the SRA Data Locator. The SDL is a place holder for the NCBI DRS service.
- A checksum was computed by the DNAStack WES implementation on the sra format file for which a URL could be obtained. Though GetObject showed there are BAM files with an access_id of gs.us URLs to these could not be obtained.
- Possible to do's

  - Substitute in SRA DRS server
  - Identify why BAM file URLS are not returned by SDL.

####  JMJD1C variants - 

Script: [FASPScript7.py](https://github.com/ga4gh/fasp-scripts/blob/master/fasp/scripts/FASPScript7.py)


- Uses the ISB-CGC BigQuery tables to query for subjects from TCGA with variants in the JMJD1C gene.  This is the gene in the example shared by Anne Deslattes Mays. This illustrates the kind of query that could be used for the workflows Anne wants to perform.

- Possible to do's


    - Substitute in SRA DRS server
    
    - Identify other GA4GH data sources that might contain relevant data for this disease.

------

## **Workflow support**

checksum.wdl - a simple workflow for testing WES submission - calculates a checksum

More to be added

## Other demos and tests

**testSearchPagination.py** - demonstrates how Discovery Seach query results are returned over several pages

**examples** - examples of using individual APIs used in the main examples 



