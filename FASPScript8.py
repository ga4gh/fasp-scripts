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
from GCPLSsamtools import GCPLSsamtools
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
	mysams = {'s3':samtoolsSBClient('cgc','forei/gecco'),
				'gs': GCPLSsamtools('gs://isbcgc-216220-life-sciences/tcgatest/')}
	
	# A log is helpful to keep track of the computes we've submitted
	pipelineLogger = FASPLogger("./output/pipelineLog.txt", os.path.basename(__file__))
	
	# repeat steps 2 and 3 for each row of the query
	commands = []
	for row in query_job:

		print("subject={}, drsID={}".format(row[0], row[1]))
		
		# Step 2 - Use DRS to get the URL
		objInfo = drsClient.getObject(row[1])
		fileSize = objInfo['size']
		outfile = "{}.txt".format(row[0])
		# submit to both aws and gcp
		for cl, mysam in mysams.items():
			url = drsClient.getAccessURL(row[1], cl)
			# Step 3 - Run a pipeline on the file at the drs url
			if cl == 'gs':
				commands.append(mysam.statsCommandLine(url, outfile))
				task_id = 'paste here'
			else:
				task = mysam.runWorkflow(url, outfile)
				task_id = task.id
			via = 'py'
			note = 'double submit'

			time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
			pipelineLogger.logRun(time, via, note,  task_id, outfile, str(fileSize),
			searchClient, drsClient, mysam)

	# Submit the jobs using our workaround
	shellscriptPath = "./workaround.sh"
	shellScript = open(shellscriptPath, "w")
	for line in commands:
  		shellScript.write(line)
  		shellScript.write("\n")
	shellScript.close()
	# finally! submit all our hard work
	subprocess.call(['sh', shellscriptPath])
	
	pipelineLogger.close()
    
if __name__ == "__main__":
    main(sys.argv[1:])
    


	
	

	
	









