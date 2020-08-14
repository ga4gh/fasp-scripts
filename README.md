# FASPclient
 Scripts and clients for GA4GH Federated Analysis Systems Project

### **Prerequisites to run**

- Python 3
  - See the code for the modules required
- A folder in your home directory called .keys containing
  - BDCcredentials.json - api_key file [obtained from BioDataCatalyst](https://gen3.biodatacatalyst.nhlbi.nih.gov/identity)
  - CRDCAPIKey.json - api_key file [obtained from Cancer Research Data Commons](https://nci-crdc.datacommons.io/identity)
- Google Life Sciences API enabled for your GCP account
- BigQuery python libraries

#### **FASPScript1.py**

A script to 

- Query for files according to subject and specimen data and obtain their DRS ids

  Currently queries BigQuery directly. Will be substituted by Discovery Search

- Get URLs for the files from the relevant DRS server

- Submit a computes on each of the files

  Currently submits directly to aGCP Life Sciences pipeline. This will be substituted by a submission to a WES server

#### **FASPScript2.py**

As above except it performs two queries as follows 

- Query 1000 Genomes data based on data from BioDataCatalyst

- Query TCGA data in the CRDC/GDC

- Both queries prepend to the ids an appropriate prefix to identify which DRS server should be called for 

  Currently submits directly to aGCP Life Sciences pipeline. This will be substituted by a submission to a WES 

#### FASPScript3.py

Same as FASPScript1.py except 

- Uses the public DNAStack Discovery Search server

#### FASPScript4.py

Same as FASPScript1.py except 

- Uses both the public DNAStack Discovery Search server and WES server. All three steps use GA4GH APIs.

#### Other demos and tests

**testSearchPagination.py** - demonstrates how query results are returned over several pages

**examples** - examples of using individual APIs used in the main examples 

### **Supporting clients**

#### **Gen3DRSClient.py**

This is a python wrapper for the two DRS functions. It also handles Gen3 authentication using Fence. This is necessary until RAS/Passport support is in place.

#### **GCPLSsamtools.py**

Wrapper to prepare a job to run samtools as a GCP Life Sciences pipeline. This will be substituted by a submission to a WES server (See WESClient.py).

#### DiscoveryClient.py

Wrapper to call a DiscoveryClient and return results of a query.

#### WESClient.py

Wrapper to make a WES call. Currently does an MD5 checksum, plan is to use samtools and eventually a GWAS workflow. 

### **Workflows**

checksum.wdl - a simple workflow for testing WES submission - calculates a checksum

More to be added



