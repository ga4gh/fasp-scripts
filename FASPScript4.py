#  IMPORTS
import sys, getopt, os
import json
import datetime
import subprocess 

from FASPRunner import FASPRunner

# The implementations we're using
from Gen3DRSClient import Gen3DRSClient
from DiscoverySearchClient import DiscoverySearchClient
from DNAStackWESClient import DNAStackWESClient


def main(argv):

	# Step 1 - Discovery
	# query for relevant DRS objects
	searchClient = DiscoverySearchClient('https://ga4gh-search-adapter-presto-public.prod.dnastack.com/')
	query = "select submitter_id, read_drs_id drsid from thousand_genomes.onek_genomes.ssd_drs where population = 'ACB' limit 1"

	# Step 2 - DRS - set up a DRS Client
	# BDC
	drsClient = Gen3DRSClient('https://gen3.biodatacatalyst.nhlbi.nih.gov/', 'user/credentials/cdis/access_token',
	'~/.keys/BDCcredentials.json', 'gs')
	
	
	# Step 3 - set up a class that run a compute for us
	wesClient = DNAStackWESClient('~/.keys/DNAStackWESkey.json')
	
	# Use this to find out the name of this file, so we can log what ran the pipeline
	thisScript =  os.path.basename(__file__)
	
	faspRunner = FASPRunner(thisScript, searchClient,
		drsClient, wesClient, "./pipelineLog.txt")
		
	faspRunner.runQuery(query, 'One k query using Search and WES')
    
if __name__ == "__main__":
    main(sys.argv[1:])
    


	
	

	
	









