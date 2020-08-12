# FASPclient
 Scripts and clients for GA4GH Federated Analysis Systems Project

**Prerequisites to run**

- Python 3
- A folder in your home directory called .keys containing
  - BDCcredentials.json - api_key file [obtained from BioDataCatalyst](https://gen3.biodatacatalyst.nhlbi.nih.gov/identity)
  - CRDCAPIKey.json - api_key file [obtained from Cancer Research Data Commons](https://nci-crdc.datacommons.io/identity)
- Google Life Sciences API enabled for your GCP account
- BigQuery python libraries

**FASPScript1.py**

A script to 

- Query for files according to subject and specimen data and obtain their DRS ids

  Currently queries BigQuery directly. Will be substituted by Discovery Search

- Get URLs for the files from the relevant DRS server

- Submit a computes on each of the files

  Currently submits directly to aGCP Life Sciences pipeline. This will be substituted by a submission to a WES 

**FASPScript2.py**

As above except it performs two queries as follows 

- Query 1000 Genomes data based on data from BioDataCatalyst

- Query TCGA data in the CRDC/GDC

- Both queries prepend to the ids an appropriate prefix to identify which DRS server should be called for 

  Currently submits directly to aGCP Life Sciences pipeline. This will be substituted by a submission to a WES 

**Supporting clients**

**Gen3DRSClient.py**

This is a python wrapper for the two DRS functions. It also handles Gen3 authentication using Fence. This is necessary until RAS/Passport support is in place.

**GCPLSsamtools**

Wrapper to prepare a job to run samtools as a GCP Life Sciences pipeline. This will be substituted by a submission to a WES server.

**Workflows**

checksum.wdl - a simple workflow for testing WES submission - calculates a checksum

More to be added



