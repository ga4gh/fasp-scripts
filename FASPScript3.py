#  IMPORTS
import sys 

from FASPRunner import FASPRunner

# The implementations we're using
from Gen3DRSClient import bdcDRSClient
from GCPLSsamtools import GCPLSsamtools
from DiscoverySearchClient import DiscoverySearchClient

def main(argv):


	faspRunner = FASPRunner("./pipelineLog.txt", pauseSecs=0)

	# Step 1 - Discovery
	# query for relevant DRS objects
	searchClient = DiscoverySearchClient('https://ga4gh-search-adapter-presto-public.prod.dnastack.com/')
	query = "select submitter_id, read_drs_id drsid from thousand_genomes.onek_genomes.ssd_drs where population = 'BEB' limit 3"

	# Step 2 - DRS - set up a DRS Client
	# CRDC
	drsClient = bdcDRSClient('~/.keys/BDCcredentials.json', 'gs')

	
	# Step 3 - set up a class that runs samtools for us
	# providing the location where we the results to go
	mysam = GCPLSsamtools(faspRunner.settings['GCPOutputBucket'])
	

	faspRunner.configure(searchClient, drsClient, mysam)
		
	faspRunner.runQuery(query, 'One k query using Search')
	    
if __name__ == "__main__":
    main(sys.argv[1:])
    


	
	

	
	









