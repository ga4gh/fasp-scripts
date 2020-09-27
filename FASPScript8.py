#  IMPORTS
import sys, os
import datetime

# a utility 
from FASPLogger import FASPLogger
from DemoCredits import Creditor

# The implementations we're using
from Gen3DRSClient import crdcDRSClient
from samtoolsSBClient import samtoolsSBClient
from GCPLSsamtools import GCPLSsamtools
from BigQuerySearchClient import BigQuerySearchClient



def main(argv):
	
	# set your Seven Bridges CGC project name here
	sbProject = 'id/project'

	# create a creditor to credit the services being called
	creditor = Creditor.creditorFactory()
	
	# Step 1 - Discovery
	# query for relevant DRS objects
	searchClient = BigQuerySearchClient()


	# Step 2 - DRS - set up a DRS Client
	drsClient = crdcDRSClient('~/.keys/CRDCAPIKey.json', 's3')

	# Step 3 - set up a class that runs samtools for us
	mysams = {'s3':samtoolsSBClient('cgc', sbProject),
				'gs': GCPLSsamtools('gs://isbcgc-216220-life-sciences/tcgatest/')}
	
	# A log is helpful to keep track of the computes we've submitted
	pipelineLogger = FASPLogger("./pipelineLog.txt", os.path.basename(__file__))
	

	query = """
     	SELECT 'case_'||associated_entities__case_gdc_id , file_id
		FROM `isb-cgc.GDC_metadata.rel24_fileData_active` 
		where data_format = 'BAM' 
		and project_disease_type = 'Breast Invasive Carcinoma'
		limit 3"""
	print(query)
	
	query_job = searchClient.runQuery(query)  # Send the query
	creditor.creditFromList('ISBGDCData')
		
	# repeat steps 2 and 3 for each row of the query

	for row in query_job:

		print("subject={}, drsID={}".format(row[0], row[1]))
		
		# Step 2 - Use DRS to get the URL
		objInfo = drsClient.getObject(row[1])
		creditor.creditClass(drsClient)
		fileSize = objInfo['size']
		outfile = "{}.txt".format(row[0])
		# submit to both aws and gcp
		for cl, mysam in mysams.items():
			url = drsClient.getAccessURL(row[1], cl)
			# Step 3 - Run a pipeline on the file at the drs url
			
			creditor.creditClass(mysam)
			task_id = mysam.runWorkflow(url, outfile)
			via = 'py'
			note = 'double submit'

			time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
			pipelineLogger.logRun(time, via, note,  task_id, outfile, str(fileSize),
			searchClient, drsClient, mysam)

	
	pipelineLogger.close()
	creditor.creditFromList('FASPScript8_sdrf', closeImage=False)
    
if __name__ == "__main__":
    main(sys.argv[1:])
    


	
	

	
	









