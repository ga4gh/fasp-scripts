#  IMPORTS
import sys, getopt, os
import json
import datetime
import subprocess 

from FASPRunner import FASPRunner
# a utility 
from FASPLogger import FASPLogger

# The implementations we're using
from Gen3DRSClient import bdcDRSClient
from Gen3DRSClient import Gen3DRSClient
from GCPLSsamtools import GCPLSsamtools
from BigQuerySearchClient import BigQuerySearchClient

def main(argv):

	# Step 1 - Discovery
	# query for relevant DRS objects
	searchClient = BigQuerySearchClient()
# 	query = """
#      	SELECT subject_id, read_drs_id
#      	FROM `isbcgc-216220.COPDGene.phenotype_drs`
#      	where weight_kg between 91.8 and 93.0
#      	LIMIT 1"""
	query = """
		SELECT submitter_id, read_drs_id
		FROM `isbcgc-216220.onek_genomes.ssd_drs`
		where population = 'BEB'
		LIMIT 3"""

	# CRDC
	#drsClient = Gen3DRSClient('https://nci-crdc.datacommons.io/', 'user/credentials/api/access_token')
	# BioDataCatalyst
	drsClient = bdcDRSClient('~/.keys/BDCcredentials.json', 'gs')
	
	
	mysam = GCPLSsamtools('gs://isbcgc-216220-life-sciences/fasand/')
	
	faspRunner = FASPRunner('FASPScript1', searchClient,
		drsClient, mysam, "./pipelineLog.txt", pauseSecs=0)
		
	faspRunner.runQuery(query, 'One k  query ')
	    
if __name__ == "__main__":
    main(sys.argv[1:])
    


	
	

	
	









