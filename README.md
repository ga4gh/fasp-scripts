# fasp-scripts
 Notebooks and clients for GA4GH Federated Analysis Systems Project

[TOC]



------

### **Prerequisites

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
  - BigQuery python libraries - for scripts that use BigQuery
  - [pyega3](https://pypi.org/project/pyega3/) - EGA client libraries for download. See also [EGA documentation for client API](https://ega-archive.org/download/downloader-quickguide-APIv3). 

------

### **Clients provided in FASP Package

### **Search clients**

#### DataConnectClient

Wrapper to call GA4GH Data Connect Servers and return results of a queries.

#### BigQuerySearchClient

Perform searches via BigQuery

------

### **DRS and 'DRS-like' clients**

#### DRSClient.py

Superclass for DRS Clients

#### **Gen3DRSClient.py**

This is a python wrapper for the two DRS functions. It also handles Gen3 authentication using Fence. This is necessary until RAS/Passport support is in place.

There are two clients for specific Gen3 DRS servers

- **crdcDRSClient** - client for Cancer Research Data Commons DRS server
- **bdcDRSClient** - client for BioDataCatalyst DRS server

#### SBDRSClient.py

A DRS client for Seven Bridges DRS services. Handles SB specific authentication. Two specific classes are provided.

- **sbcgcDRSClient** - client for Seven Bridges Cancer Genomics Cloud DRS server 
- **cavaticaDRSClient**  - client for Cavatica DRS Server

#### sdlDRSClient.py

A DRS-like wrapper around the SRA Data Locator. Uses standard dbGaP/SRA authentication (.ngc file)

------



### WES clients

#### DNAStackWESClient.py

Wrapper to make a WES call. Currently does an MD5 checksum and the plenary GWAS workflow. The plan is to use samtools and eventually a GWAS workflow. 

#### sb_wes_client.py

Client to call Seven Bridges WES Servers. The specific features addressed include authentication, setting a project to work within and the use of apps stored in the Seven Bridges environment. For testing and demo purposes this client encapsulates running samtools. 

#### elixir_wes_client.py

Client to call Elixir WES Servers. The specific features addressed include authentication, setting a project to work within and the use of apps stored in the Seven Bridges environment. For testing and demo purposes this client encapsulates running samtools. 

#### WESClient.py

Superclass for WES clients. Has generic capability to run WES requiring full configuration of the request body and possibly knowledge of the specific WES server being called.

### Other Workflow clients

These provide a WES like binding to proprietary APIs so that capabilities can be explored where no WES implentation so far exists.

#### **GCPLSsamtools.py**

Wrapper to prepare a job to run samtools as a GCP Life Sciences pipeline. 

Requires: Google Life Sciences API installed and configured for your GCP account

#### SBsamtools.py

Submits a samtools stats task via Seven Bridges API. By preference should now use the SB WES Client

Requires: Seven Bridges API Python client installed and configured for your GCP account

#### 

------

### **Workflow support**

checksum.wdl - a simple workflow for testing WES submission - calculates a checksum

More to be added

#### Other demos and tests

**testSearchPagination.py** - demonstrates how Discovery Seach query results are returned over several pages

**examples** - examples of using individual APIs used in the main examples 



