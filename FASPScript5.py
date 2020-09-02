#  IMPORTS
import sys, getopt, os
import json
import datetime
import subprocess 

# a utility 
from FASPRunner import FASPRunner

# The implementations we're using
from Gen3DRSClient import crdcDRSClient
from samtoolsSBClient import samtoolsSBClient
from BigQuerySearchClient import BigQuerySearchClient



def main(argv):

	# Step 1 - Discovery
	# query for relevant DRS objects
	searchClient = BigQuerySearchClient()

	query = """
     	SELECT 'case_'||associated_entities__case_gdc_id , file_id
		FROM `isb-cgc.GDC_metadata.rel24_fileData_active` 
		where data_format = 'BAM' 
		and project_disease_type = 'Breast Invasive Carcinoma'
		limit 3"""
	
	drsClient = crdcDRSClient('~/.keys/CRDCAPIKey.json', 's3')

	
	
	# Step 3 - set up a class that runs samtools for us
	mysam = samtoolsSBClient('cgc','forei/gecco')
	
	# Use this to find out the name of this file, so we can log what ran the pipeline
	thisScript =  os.path.basename(__file__)
	
	faspRunner = FASPRunner(thisScript, searchClient,
		drsClient, mysam, "./pipelineLog.txt")
		
	faspRunner.runQuery(query, 'GDC query SB compute')
	    
if __name__ == "__main__":
    main(sys.argv[1:])
    


	
	

	
	









