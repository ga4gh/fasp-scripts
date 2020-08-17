#  IMPORTS
import sys, getopt, os
import json
import datetime
import subprocess 

# a utility 
from FASPLogger import FASPLogger

# The implementations we're using
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
		LIMIT 1"""

	query_job = searchClient.runQuery(query)  # Send the query
	
	# Step 2 - DRS - set up a DRS Client
	# CRDC
	#drsClient = Gen3DRSClient('https://nci-crdc.datacommons.io/', 'user/credentials/api/access_token')
	# BioDataCatalyst
	drsClient = Gen3DRSClient('https://gen3.biodatacatalyst.nhlbi.nih.gov/', 'user/credentials/cdis/access_token',
	'~/.keys/BDCcredentials.json')
	
	
	# Step 3 - set up a class that runs samtools for us
	# providing the location where we the results to go
	mysam = GCPLSsamtools('gs://isbcgc-216220-life-sciences/fasand/')
	
	# workaround - see below
	commands = []
	
	# A log is helpful to keep track of the computes we've submitted
	pipelineLogger = FASPLogger("./pipelineLog.txt", os.path.basename(__file__))
	
	# repeat steps 2 and 3 for each row of the query
	for row in query_job:

		print("subject={}, drsID={}".format(row[0], row[1]))
		
		# Step 2 - Use DRS to get the URL
		objInfo = drsClient.getObject(row[1])
		fileSize = objInfo['size']
		# we've predetermined we want to use the gs copy in this case
		url = drsClient.getAccessURL(row[1], 'gs')
		
		# Step 3 - Run a pipeline on the file at the drs url
		outfile = "{}.txt".format(row[0])
		#This should have allowed us to submit a pipeline - but the pipelines fail
		#response = mysam.runStats(url, outfile)
		#pipeline_id = response['name']
		# via = 'py'
		# This is the workaround - just create a shell script
		commands.append(mysam.statsCommandLine(url, outfile))
		via = 'sh'
		pipeline_id = 'paste here'
		note = ''

		time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
		pipelineLogger.logRun(time, via, note,  pipeline_id, outfile, str(fileSize),
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
    


	
	

	
	









