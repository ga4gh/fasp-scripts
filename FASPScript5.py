#  IMPORTS
import sys, getopt, os
import json
import datetime
import subprocess 

# a utility 
from FASPLogger import FASPLogger

# The implementations we're using
from Gen3DRSClient import Gen3DRSClient
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

	query_job = searchClient.runQuery(query)  # Send the query
	
	# Step 2 - DRS - set up a DRS Client
	crdcBase = 'https://nci-crdc.datacommons.io/'
	drsClient = Gen3DRSClient(crdcBase, 'user/credentials/api/access_token',
	'~/.keys/CRDCAPIKey.json')

	
	
	# Step 3 - set up a class that runs samtools for us
	mysam = samtoolsSBClient('cgc','forei/gecco')
	
	# A log is helpful to keep track of the computes we've submitted
	pipelineLogger = FASPLogger("./pipelineLog.txt", os.path.basename(__file__))
	
	# repeat steps 2 and 3 for each row of the query
	for row in query_job:

		print("subject={}, drsID={}".format(row[0], row[1]))
		
		# Step 2 - Use DRS to get the URL
		objInfo = drsClient.getObject(row[1])
		fileSize = objInfo['size']
		# we've predetermined we want to use the gs copy in this case
		url = drsClient.getAccessURL(row[1], 's3')
		
		# Step 3 - Run a pipeline on the file at the drs url
		outfile = "{}.txt".format(row[0])
		task = mysam.runWorkflow(url)
		via = 'py'
		note = 'Discovery Search-SBG-cgc compute w looger'

		time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
		pipelineLogger.logRun(time, via, note,  task.id, outfile, str(fileSize),
			searchClient, drsClient, mysam)

	
	pipelineLogger.close()
    
if __name__ == "__main__":
    main(sys.argv[1:])
    


	
	

	
	









