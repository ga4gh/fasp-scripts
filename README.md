# FASPclient
 Scripts and clients for GA4GH Federated Analysis Systems Project



**FASPScript1.py**

A script to 

- Query for files according to subject and specimen data and obtain their DRS ids

  Currently queries BigQuery directly. Will be substituted by Discovery Search

- Get URLs for the files from the relevant DRS server

- Submit a computes on each of the files

  Currently submits directly to aGCP Life Sciences pipeline. This will be substituted by a submission to a WES 

Supporting clients

**Gen3DRSClient.py**

Obtain an access key from a Gen3 DRS server using Fence authentication.

Make DRS calls

**GCPLSsamtools**

Wrapper to prepare a job to run samtools as a GCP Life Sciences pipeline. This will be substituted by a submission to a WES server.



