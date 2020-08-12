#  IMPORTS
from google.cloud import bigquery
import sys, getopt
import os.path
import json
import datetime
import subprocess 

from Gen3DRSClient import Gen3DRSClient
from GCPLSsamtools import GCPLSsamtools
from MyMetaResolver import MyMetaResolver

def runQuery(query):
	bqclient = bigquery.Client()
	query_job = bqclient.query(query)  # Send the query
	queryResults = []
	for row in query_job:
		queryResults.append(row)
		print("subject={}, drsID={}".format(row[0], row[1]))
	return queryResults
	

def main(argv):

	# Step 1 - Discovery
	# query for relevant DRS objects

	crdcquery = """
     	SELECT 'case_'||associated_entities__case_gdc_id , 'crdc:'||file_id
		FROM `isb-cgc.GDC_metadata.rel24_fileData_active` 
		where data_format = 'BAM' 
		and project_disease_type = 'Breast Invasive Carcinoma'
		limit 3"""
	bdcquery = """
  		SELECT submitter_id, 'bdc:'||read_drs_id
  		FROM `isbcgc-216220.1000Genomes.ssd_drs_table`
      	where population = 'ACB'
      	LIMIT 3"""

	results = runQuery(crdcquery)  # Send the query
	results += runQuery(bdcquery)  
	

	# Step 2 - DRS - set up DRS Clients
	
	# For later!
	# mr = MyMetaResolver()
	
	# CRDC
	crdcBase = 'https://nci-crdc.datacommons.io/'
	crdcdrsClient = Gen3DRSClient(crdcBase, 'user/credentials/api/access_token',
	'~/.keys/CRDCAPIKey.json')
	# BioDataCatalyst
	bdcBase = 'https://gen3.biodatacatalyst.nhlbi.nih.gov/'
	bdcdrsClient = Gen3DRSClient(bdcBase, 'user/credentials/cdis/access_token',
	'~/.keys/BDCcredentials.json')
	
	drsClients = {
		"crdc": crdcdrsClient,
		"bdc": bdcdrsClient
	}
	
	# Step 3 - set up a class that runs samtools for us
	# providing the location for the results
	mysam = GCPLSsamtools('gs://isbcgc-216220-life-sciences/fasand/')
	
	# A log is helpful to keep track of the computes we've submitted
	pipelineLog = open("./pipelineLog.txt", "a")

	# repeat steps 2 and 3 for each row of the query
	commands = []
	for row in results:

		print("subject={}, drsID={}".format(row[0], row[1]))
		
		# Step 2 - Use DRS to get the URL
		# get the prefix
		prefix, drsid = row[1].split(":", 1)
		url = drsClients[prefix].getAccessURL(drsid, 'gs')
		
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

	# workaround - see below
	commands = []
	
	

    
if __name__ == "__main__":
    main(sys.argv[1:])
    


	
	

	
	









