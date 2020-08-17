# FASPclient
 Scripts and clients for GA4GH Federated Analysis Systems Project

[TOC]



------

### **Prerequisites to run**

- Python 3
  - See the code for the modules required
- A folder in your home directory called .keys containing
  - BDCcredentials.json - api_key file [obtained from BioDataCatalyst](https://gen3.biodatacatalyst.nhlbi.nih.gov/identity)
  - CRDCAPIKey.json - api_key file [obtained from Cancer Research Data Commons](https://nci-crdc.datacommons.io/identity)
- Google Life Sciences API enabled for your GCP account
- BigQuery python libraries

------

#### Thousand Genomes FASP

This queries Thousand Genomes data on subjects and specimens which was exported from BioDataCatalyst and loaded into BigQuery.

Scripts: FASPScript1.py, FASPScript3.py, FASPScript4.py

- All three scripts perform the following
   - Query for files according to subject and specimen data and obtain their DRS ids
   - Get URLs for the files from the relevant DRS server
   - Submit a compute on each of the files
- [FASPScript4](https://github.com/ianfore/FASPclient/blob/master/FASPScript4.py) uses the following GA4GH APIs to perform each step
   - Discovery Search Server (DNA Stack) - Presto on BigQuery
   - DRS server (BioDataCatalyst)
   - WES Server (DNA Stack)

The other two scripts were proof of concept using direct APIs from different stacks
 - [FASPScript1](https://github.com/ianfore/FASPclient/blob/master/FASPScript1.py) uses BigQuery for the query and directly submits a GCP Life Sciences pipeline for the compute. This compute uses samtools stats.
 - [FASPScript3](https://github.com/ianfore/FASPclient/blob/master/FASPScript3.py) is the same as but substitutes in public DNAStack Discovery Search server for search

- Possible to do's

  - Troubleshoot samtools stats workflow on DNAStack WES server 
  - Configure additional tables on DNAStack Search server 
  - Add compute on Seven Bridges platform - see below

#### Demonstration of Search and compute from multiple sources 

Script: [FASPScript2.py](https://github.com/ianfore/FASPclient/blob/master/FASPScript2.py)


- Query COPDGene data in BigQuery, exported from BioDataCatalyst via PFB.

- Query TCGA data in the ISB-CGC tables in BigQuery,

- Both queries use an appropriate prefix to identify which DRS server should be called to obtain a url to the file.

  Currently submits directly to aGCP Life Sciences pipeline. This will be substituted by a submission to a WES Server.
  
  Both datasets are contolled access data. Access is controlled by the respective Fence access tokens on the CRDC and BioDataCatalyst DRS servers. The COPD data in BigQuery is under GCP IAM access control.




- Possible to do's

  - Add additional dbGaP datasets.
  - Move query to Discovery Search - requires access control on Discovery Search.

#### Compute on AWS via different stack 

Script: [FASPScript5.py](https://github.com/ianfore/FASPclient/blob/master/FASPScript5.py)


- Some of the files returned from DRS for the queries above have files on AWS. This script used the Seven Bridges API to run samtools stats on those files.
- Though the tasks are submitted, they fail with a "Protocol not supprted" error.  See [issue](https://github.com/ga4gh/cloud-interop-testing/issues/109).
- Possible to do's

  - Update samtools docker image to one that can use a url.
  - Use a Seven Bridges WES implementation which can either accept the signed URL, or take DRS ids.

#### Compute on SRA urls 

Script: [FASPScript6.py](https://github.com/ianfore/FASPclient/blob/master/FASPScript6.py)


- This script demonstrates that the DNAStack WES Server can perform a compute on the urls returned by the SRA Data Locator. The SDL is a place holder for the NCBI DRS service.
- A checksum was computed on the sra format file for which a URL could be obtained. Though GetObject showed there are BAM files with an access_id of gs.us URLs to these could not be obtained.
- Possible to do's

  - Substitute in SRA DRS server
  - Identify why BAM file URLS are not returned by SDL.

####  JMJD1C variants - 

Script: [FASPScript7.py](https://github.com/ianfore/FASPclient/blob/master/FASPScript7.py)


- Uses the ISB-CGC BigQuery tables to query for subjects from TCGA with variants in the JMJD1C gene.  This is the gene in the example shared by Anne Deslattes Mays. This illustrates the kind of query 

- This script also introduces a FASPRunner1 class to hide the underlying steps and allow focus on the query

- Possible to do's


  - Substitute in SRA DRS server

  - Identify other GA4GH data sources that might contain relevant data for this disease.

  - Refactor FASPRunner1 to an abstract FASPRunner class. The abstract class could be configured dynamically to use the clients of choice for each step of the FASP sequence.

    

####  Simulate identifiers.org/n2t.net - 

Script: [MyMetaResolver.py](https://github.com/ianfore/FASPclient/blob/master/FASPScript7.py)


- Simulates how compact identifier prefixing can be used to redirect DRS GetObject calls to the right DRS Server.
- Possible to do's

  - Do trial registration of DRS server prefixes
  - Provide feedback on spec.
  - Explore prefixing best practices.

------

### **Supporting clients**

### **Search clients**

#### DiscoverySearchClient.py

Wrapper to call the DNAStack DiscoveryClient and return results of a query.

#### BigQuerySearchClient

Perform searches via BigQuery

------

### **DRS and 'DRS-like' clients**

#### DRSClient.py

Super class for DRS Clients

#### **Gen3DRSClient.py**

This is a python wrapper for the two DRS functions. It also handles Gen3 authentication using Fence. This is necessary until RAS/Passport support is in place.

There are two clients for specific Gen3 DRS servers

- **crdcDRSClient** - client for Cancer Research Data Commons DRS server
- **bdcDRSClient** - client for BioDataCatalyst DRS server

#### SBDRSClient.py

A DRS client for Seven Bridges DRS services. Handles SB specific authentication

#### sdlDRSClient.py

A DRS-like wrapper around the SRA Data Locator. Uses standard dbGaP/SRA authentication (.ngc file)

------



### Workflow clients

#### DNAStackWESClient.py

Wrapper to make a WES call. Currently does an MD5 checksum, plan is to use samtools and eventually a GWAS workflow. 

#### **GCPLSsamtools.py**

Wrapper to prepare a job to run samtools as a GCP Life Sciences pipeline. 

#### SBsamtools.py

Submits a samtools stats task via Seven Bridges API

#### WESClient.py

Superclass for WES clients

------

### **Workflow support**

checksum.wdl - a simple workflow for testing WES submission - calculates a checksum

More to be added

#### Other demos and tests

**testSearchPagination.py** - demonstrates how Discovery Seach query results are returned over several pages

**examples** - examples of using individual APIs used in the main examples 



