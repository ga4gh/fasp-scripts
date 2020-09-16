#  IMPORTS
#from google.cloud import bigquery
import sys, getopt
import os.path
import json
import datetime
import subprocess 
import pandas as pd

# a utility 
from FASPLogger import FASPLogger
from DemoCredits import Creditor

# The implementations we're using
from Gen3DRSClient import crdcDRSClient
from Gen3DRSClient import bdcDRSClient
from SBDRSClient import sbcgcDRSClient
from GCPLSsamtools import GCPLSsamtools
from samtoolsSBClient import samtoolsSBClient
from BigQuerySearchClient import BigQuerySearchClient



def main(argv):


	# create a creditor to credit the services being called
	creditor = Creditor.creditorFactory()
	
	# Step 1 - Discovery
	# query for relevant DRS objects
	searchClient = BigQuerySearchClient()

	crdcquery = """
		SELECT sp.dbGaP_Subject_ID,  'sb:'||sb_drs_id
		FROM `isbcgc-216220.scr_GECCO_CRC_Susceptibility.Subject_Phenotypes_MULTI` sp
		join `isbcgc-216220.scr_GECCO_CRC_Susceptibility.Sample_MULTI` sm on sm.dbgap_subject_id = sp.dbgap_subject_id
		join `isbcgc-216220.scr_GECCO_CRC_Susceptibility.sb_drs_index` di on di.sample_id = sm.sample_id
		where AGE between 45 and 55
		and sex = 'Female'
		and file_type = 'cram'
		limit 3"""
		
	bdcquery = """
		SELECT sp.dbGaP_Subject_ID,  'bdc:'||read_drs_id
		FROM `isbcgc-216220.COPDGene.Subject_MULTI` sm
		join `isbcgc-216220.COPDGene.Subject_Phenotypes_HMB` sp on sp.dbgap_subject_id = sm.dbgap_subject_id
		join `isbcgc-216220.COPDGene.COPD_DRS` drs on drs.su_submitter_id = sm.subject_id
 		where gender = '2'
 		and Age_Enroll between 45 and 55
 		LIMIT 3"""
		

	results = searchClient.runQuery(crdcquery)  # Send the query
	creditor.creditFromList('dbGapSSD')
	results += searchClient.runQuery(bdcquery) 
	creditor.creditFromList('BDCData')
	

	# Step 2 - DRS - set up DRS Clients	
	drsClients = {
		"sb": sbcgcDRSClient('~/.keys/sevenbridges_keys.json', 's3'),
		"bdc": bdcDRSClient('~/.keys/BDCcredentials.json', 'gs')
	}
	print('setting credentials ')
	creditor.creditFromList('dbGaPFence')
		
	# Step 3 - set up a class that runs samtools for us
	# providing the location for the results
	samClients = {
		"sb": samtoolsSBClient('cgc', 'forei/gecco'),
		"bdc": GCPLSsamtools('gs://isbcgc-216220-life-sciences/fasand/')
	}

	
	# A log is helpful to keep track of the computes we've submitted
	pipelineLogger = FASPLogger("./pipelineLog.txt", os.path.basename(__file__))
	
	# repeat steps 2 and 3 for each row of the query
	for row in results:

		print("subject={}, drsID={}".format(row[0], row[1]))
		resRow = [row[0], row[1]]
		# Step 2 - Use DRS to get the URL
		# get the prefix
		prefix, drsid = row[1].split(":", 1)
		drsClient = drsClients[prefix]
		creditor.creditClass(drsClient)
		url = drsClient.getAccessURL(drsid)
		#objInfo = drsClient.getObject(drsid)
		#print (objInfo)
		#fileSize = objInfo['size']
		fileSize = 0
				
		# Step 3 - Run a pipeline on the file at the drs url
		if url != None:
			outfile = "{}.txt".format(row[0])
			mysam = samClients[prefix]
			creditor.creditClass(mysam)
			via = 'sh'
			note = 'Two dbGaP sources'
			time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
			run_id = mysam.runWorkflow(url, outfile)
			pipelineLogger.logRun(time, via, note,  run_id, outfile, fileSize,
				searchClient, drsClient, mysam)
			resRow.append('OK')
		else:
			print('could not get DRS url')
			resRow.append('unauthorized')

			
	pipelineLogger.close()
    
if __name__ == "__main__":
    main(sys.argv[1:])
    


	
	

	
	









