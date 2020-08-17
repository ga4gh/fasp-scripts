#  IMPORTS
#from google.cloud import bigquery
import sys, getopt
import os.path
import json
import datetime
import subprocess 

# a utility 
from FASPLogger import FASPLogger

# The implementations we're using
from Gen3DRSClient import crdcDRSClient
from Gen3DRSClient import bdcDRSClient
from GCPLSsamtools import GCPLSsamtools
from BigQuerySearchClient import BigQuerySearchClient



def main(argv):

	# Step 1 - Discovery
	# query for relevant DRS objects
	searchClient = BigQuerySearchClient()

	crdcquery = """
     	SELECT 'case_'||associated_entities__case_gdc_id , 'crdc:'||file_id
		FROM `isb-cgc.GDC_metadata.rel24_fileData_active` 
		where data_format = 'BAM' 
		and project_disease_type = 'Breast Invasive Carcinoma'
		limit 3"""
	bdcquery = """
  		SELECT SUBJECT_ID, 'bdc:'||read_drs_id
  		FROM `isbcgc-216220.COPDGene.phenotype_drs`
      	where Weight_KG between 92.5 and 93.0
      	LIMIT 3"""
  		#FROM `isbcgc-216220.1000Genomes.ssd_drs_table`
  		
	results = searchClient.runQuery(crdcquery)  # Send the query
	results += searchClient.runQuery(bdcquery)  
	

	# Step 2 - DRS - set up DRS Clients
	
	# For later!
	# mr = MyMetaResolver()
	
	drsClients = {
		"crdc": crdcDRSClient('~/.keys/CRDCAPIKey.json'),
		"bdc": bdcDRSClient('~/.keys/BDCcredentials.json')
	}
	
	# Step 3 - set up a class that runs samtools for us
	# providing the location for the results
	mysam = GCPLSsamtools('gs://isbcgc-216220-life-sciences/fasand/')
	
	# A log is helpful to keep track of the computes we've submitted
	pipelineLogger = FASPLogger("./pipelineLog.txt", os.path.basename(__file__))
	
	# repeat steps 2 and 3 for each row of the query
	commands = []
	for row in results:

		print("subject={}, drsID={}".format(row[0], row[1]))
		
		# Step 2 - Use DRS to get the URL
		# get the prefix
		prefix, drsid = row[1].split(":", 1)
		url = drsClients[prefix].getAccessURL(drsid, 'gs')
		drsClient = drsClients[prefix]
		objInfo = drsClient.getObject(drsid)
		fileSize = objInfo['size']
				
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
		note = 'Two sources'
		time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
		pipelineLogger.logRun(time, via, note,  pipeline_id, outfile, fileSize,
			searchClient, drsClient, mysam)
			
	# Submit the jobs using our workaround
	shellscriptPath = "./workaround.sh"
	shellScript = open(shellscriptPath, "w")
	for line in commands:
  		shellScript.write(line)
  		shellScript.write("\n")
	shellScript.close()
	subprocess.call(['sh', shellscriptPath])


	pipelineLogger.close()
    
if __name__ == "__main__":
    main(sys.argv[1:])
    


	
	

	
	









