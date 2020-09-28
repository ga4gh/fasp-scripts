#  IMPORTS
import sys, os
import datetime

# a utility 
from FASPLogger import FASPLogger

# The implementations we're using
from sdlDRSClient import sdlDRSClient
from DiscoverySearchClient import DiscoverySearchClient
from DNAStackWESClient import DNAStackWESClient


def main(argv):

	# Step 1 - Discovery
	# query for relevant DRS objects
	searchClient = DiscoverySearchClient('https://ga4gh-search-adapter-presto-public.prod.dnastack.com/')
	query = "select submitter_id, read_drs_id drsid from thousand_genomes.onek_genomes.ssd_drs where population = 'ACB' limit 1"
	query_job = searchClient.runQuery(query)

	# Step 2 - DRS - set up a DRS Client
	# CRDC
	drsClient = sdlDRSClient('~/.keys/prj_11218_D17199.ngc')
	
	# Step 3 - set up a class that run a compute for us
	wesClient = DNAStackWESClient('~/.keys/DNAStackWESkey.json')
	
	# A log is helpful to keep track of the computes we've submitted
	pipelineLogger = FASPLogger("./pipelineLog.txt", os.path.basename(__file__))
	
	# repeat steps 2 and 3 for each row of the query
	for row in query_job:

		print("subject={}, drsID={}".format(row[0], row[1]))
		
		# Step 2 - Use DRS to get the URL
		#objInfo = drsClient.getObject(row[1])
		# for testing
		acc = 'SRR5368359.sra'
		objInfo = drsClient.getObject(acc)
		fileSize = objInfo['size']
		print(fileSize)
		# we've predetermined we want to use the gs copy in this case
		#url = drsClient.getAccessURL(row[1], 'gs')
		res = drsClient.getAccessURL(acc,'gs.us')
		url = res['url']
		print(url)
		# Step 3 - Run a pipeline on the file at the drs url
		outfile = "{}.txt".format(row[0])
		pipeline_id = wesClient.runWorkflow(url, outfile)
		print('submitted:{}'.format(pipeline_id))
		
		via = 'WES'
		note = 'WES MD5 on NCBI SDL'

		time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
		pipelineLogger.logRun(time, via, note,  pipeline_id, outfile, str(fileSize),
			searchClient, drsClient, wesClient)

	
	pipelineLogger.close()
    
if __name__ == "__main__":
    main(sys.argv[1:])
    


	
	

	
	









