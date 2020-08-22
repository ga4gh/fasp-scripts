#  IMPORTS
import sys, getopt, os
import json
import datetime
import subprocess 

# a utility 
from FASPLogger import FASPLogger

# The implementations we're using
from Gen3DRSClient import bdcDRSClient
from BigQuerySearchClient import BigQuerySearchClient
from DNAStackWESClient import DNAStackWESClient


def main(argv):

	# Step 1 - Discovery
	# query for relevant DRS objects
	searchClient = BigQuerySearchClient()

	query = """
     	SELECT file, drs_id
		FROM `isbcgc-216220.onek_genomes.onek_drs` 
		where file = 'tutorial-synthetic_data_set_1' 
		"""

	query_job = searchClient.runQuery(query)  # Send the query

	# Step 2 - DRS - set up a DRS Client
	# CRDC
	drsClient = bdcDRSClient('~/.keys/BDCcredentials.json')
	
	
	# Step 3 - set up a class that run a compute for us
	wesClient = DNAStackWESClient('~/.keys/DNAStackWESkey.json')
	
	# A log is helpful to keep track of the computes we've submitted
	pipelineLogger = FASPLogger("./pipelineLog.txt", os.path.basename(__file__))
	
	# repeat steps 2 and 3 for each row of the query
	for row in query_job:
		drs_id = row[1]
		print("vcffile={}, drsID={}".format(row[0], drs_id))
		
		# Step 2 - Use DRS to get the URL
		objInfo = drsClient.getObject(drs_id)
		fileSize = objInfo['size']

		vcfurl = drsClient.getAccessURL(drs_id, 'gs')
		
		# Step 3 - Run a pipeline on the file at the drs url
		resp = wesClient.runGWASWorkflow(vcfurl, 'gs://dnastack-public-bucket/thousand_genomes_meta.csv')
		print (resp)
		pipeline_id = resp.json()['run_id']
		print('submitted:{}'.format(pipeline_id))
		
		outfile = ''
		via = 'WES'
		note = 'GWAS'

		time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
		pipelineLogger.logRun(time, via, note,  pipeline_id, outfile, str(fileSize),
			searchClient, drsClient, wesClient)

	
	pipelineLogger.close()
    
if __name__ == "__main__":
    main(sys.argv[1:])
    


	
	

	
	









