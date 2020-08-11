#  IMPORTS
from google.cloud import bigquery
import sys, getopt
import os.path
import json
import datetime
import subprocess 

from Gen3DRSClient import Gen3DRSClient
from GCPLSsamtools import GCPLSsamtools



def main(argv):

	# Step 1 - Discovery
	# query for relevant DRS objects
	bqclient = bigquery.Client()
	query = """
     	SELECT subject_id, read_drs_id
     	FROM `isbcgc-216220.COPDGene.phenotype_drs`
     	where weight_kg between 93.8 and 94.0
     	LIMIT 5"""
# 	query = """
#  		SELECT submitter_id, read_drs_id
#  		FROM `isbcgc-216220.1000Genomes.phenotype_drs`
#      	where population = 'ESN'
#      	LIMIT 1"""

	query_job = bqclient.query(query)  # Send the query
	
	# Step 2 - DRS - set up a DRS Client
	# CRDC
	#drsServer = Gen3DRSClient('https://nci-crdc.datacommons.io/', 'user/credentials/api/access_token')
	# BioDataCatalyst
	api_key_path = os.path.expanduser('~/.keys/BDCcredentials.json')
	drsServer = Gen3DRSClient('https://gen3.biodatacatalyst.nhlbi.nih.gov/', 'user/credentials/cdis/access_token')
	with open(api_key_path) as f:
		api_key = json.load(f)
	access_token = drsServer.getAccessToken(api_key)
	
	
	# Step 3 - set up a class that runs samtools for us
	# providing the location where we the results to go
	mysam = GCPLSsamtools('gs://isbcgc-216220-life-sciences/fasand/')
	
	# workaround - see below
	commands = []
	
	# A log is helpful to keep track of the computes we've submitted
	pipelineLog = open("./pipelineLog.txt", "a")
	
	# repeat steps 2 and 3 for each row of the query
	for row in query_job:

		print("subject={}, drsID={}".format(row[0], row[1]))
		
		# Step 2 - Use DRS to get the URL
		url = drsServer.getAccessURL(row[1], 'gs')
		
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
		logline = '{}\t\t{}\t{}\t{}\t{}'.format(time, via, note, pipeline_id, outfile)
		pipelineLog.write(logline)

		pipelineLog.write("\n")

	# Submit the jobs using our workaround
	shellscriptPath = "./workaround.sh"
	shellScript = open(shellscriptPath, "w")
	for line in commands:
  		shellScript.write(line)
  		shellScript.write("\n")
	shellScript.close()
	subprocess.call(['sh', shellscriptPath])
	
	pipelineLog.close()
    
if __name__ == "__main__":
    main(sys.argv[1:])
    


	
	

	
	









