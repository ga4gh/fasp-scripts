#  IMPORTS
import sys, getopt, os
import json
import datetime
import subprocess 

from Gen3DRSClient import Gen3DRSClient
from DiscoverySearchClient import DiscoverySearchClient
from WESClient import WESClient


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
	
	
	# Step 3 - set up a class that run a compute for us
	wesClient = WESClient('https://ddap-wes-service.prod.dnastack.com/ga4gh/wes/v1/runs', '~/.keys/DNAStackWESkey.json')
	
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
		resp = wesClient.runWorkflow(url)
		pipeline_id = resp.json()['run_id']
		print('submitted:{}'.format(pipeline_id))
		
		via = 'WES'
		note = 'WES MD5 from Discovery Search'

		time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
		me = os.path.basename(__file__)
		logline = '{}\t\t{}\t{}\t{}\t{}\t{}\t{}'.format(time, via, me, note, pipeline_id, outfile, fileSize)
		pipelineLog.write(logline)
		pipelineLog.write("\n")

	
	pipelineLog.close()
    
if __name__ == "__main__":
    main(sys.argv[1:])
    


	
	

	
	









