#  IMPORTS
import sys, getopt, os
import json
import datetime
import subprocess 

from Gen3DRSClient import Gen3DRSClient
from GCPLSsamtools import GCPLSsamtools
from DiscoverySearchClient import DiscoverySearchClient



def main(argv):

	# Step 1 - Discovery
	# query for relevant DRS objects
	searchClient = DiscoverySearchClient('https://ga4gh-search-adapter-presto-public.prod.dnastack.com/')
	query = "select submitter_id, read_drs_id drsid from thousand_genomes.onek_genomes.ssd_drs where population = 'BEB' limit 3"
	query_job = searchClient.runQuery(query)

	# Step 2 - DRS - set up a DRS Client
	# CRDC
	drsClient = Gen3DRSClient('https://gen3.biodatacatalyst.nhlbi.nih.gov/', 'user/credentials/cdis/access_token',
	'~/.keys/BDCcredentials.json')
	
	
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
		note = 'Discovery Search'

		time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
		me = os.path.basename(__file__)
		logline = '{}\t\t{}\t{}\t{}\t{}\t{}\t{}'.format(time, via, me, note, pipeline_id, outfile, fileSize)
		pipelineLog.write(logline)
		pipelineLog.write("\n")

	# Submit the jobs using our workaround
	shellscriptPath = "./workaround.sh"
	shellScript = open(shellscriptPath, "w")
	for line in commands:
  		shellScript.write(line)
  		shellScript.write("\n")
	shellScript.close()
	# finally! submit all our hard work
	subprocess.call(['sh', shellscriptPath])
	
	pipelineLog.close()
    
if __name__ == "__main__":
    main(sys.argv[1:])
    


	
	

	
	









