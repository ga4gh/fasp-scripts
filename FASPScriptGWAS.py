#  IMPORTS
import sys, getopt, os
import json
import datetime
import subprocess 

# a utility 
from FASPLogger import FASPLogger
from DemoCredits import Creditor

# The implementations we're using
from DRSMetaResolver import DRSMetaResolver
from DiscoverySearchClient import DiscoverySearchClient
from DNAStackWESClient import DNAStackWESClient


def main(argv):
	# create a creditor to credit the services being called
	creditor = Creditor.creditorFactory()
	
	# Step 1 - Discovery
	# query for relevant DRS objects
	searchClient = DiscoverySearchClient('https://ga4gh-search-adapter-presto-public.prod.dnastack.com/', debug=False)

	query = "SELECT file_name, compact_drs_id, hostbased_drs_id, drs_id from thousand_genomes.onek_genomes.onek_recal_variants_drs where chromosome = 'chr21' and annotated = false"
	print(query)
	
	query_job = searchClient.runQuery(query)  # Send the query
	creditor.creditClass(searchClient)
	
	# Step 2 - DRS - use the MetaResolver send drs ids to the right service
	drsResolver = DRSMetaResolver()	
	
	# Step 3 - set up a class that run a compute for us
	wesClient = DNAStackWESClient('~/.keys/DNAStackWESkey.json', debug=False)
	
	# A log is helpful to keep track of the computes we've submitted
	pipelineLogger = FASPLogger("./pipelineLog.txt", os.path.basename(__file__))
	
	# repeat steps 2 and 3 for each row of the query
	# this example should find id's for the same file in both BioDataCatalyst and Anvil
	for row in query_job:
		drs_id = row[1]
		print("vcffile={}, compact drsID={}".format(row[0], drs_id))
		
		# Step 2 - Use DRS to get the URL
		objInfo = drsResolver.getObject(drs_id)
		drsClient, id = drsResolver.getClient(drs_id)
		print(drsClient)
		creditor.creditClass(drsClient)
		fileSize = objInfo['size']

		vcfurl = drsResolver.getAccessURL(drs_id, 'gs')
		# Step 3 - Run a pipeline on the file at the drs url
		pipeline_id = wesClient.runGWASWorkflow(vcfurl, 'gs://dnastack-public-bucket/thousand_genomes_meta.csv')
		creditor.creditClass(wesClient)
		print('submitted:{}'.format(pipeline_id))
		
		outfile = ''
		via = 'WES'
		note = 'GWAS'

		time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
		pipelineLogger.logRun(time, via, note,  pipeline_id, outfile, str(fileSize),
			searchClient, drsClient, wesClient)

	
	pipelineLogger.close()
    
if __name__ == "__main__":
    main(sys.argv[1:])
    


	
	

	
	









