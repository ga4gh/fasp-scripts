#  IMPORTS
import sys 

from FASPRunner import FASPRunner

# The implementations we're using
from Gen3DRSClient import bdcDRSClient
from DiscoverySearchClient import DiscoverySearchClient
from DNAStackWESClient import DNAStackWESClient


def main(argv):

	faspRunner = FASPRunner("./pipelineLog.txt", pauseSecs=0)

	# Step 1 - Discovery
	# query for relevant DRS objects
	searchClient = DiscoverySearchClient('https://ga4gh-search-adapter-presto-public.prod.dnastack.com/')
	query = "select submitter_id, read_drs_id drsid from thousand_genomes.onek_genomes.ssd_drs where population = 'ACB' limit 3"
	
	# Step 2 - DRS - set up a DRS Client
	drsClient = bdcDRSClient('~/.keys/BDCcredentials.json', 'gs')

	# Step 3 - set up a class that run a compute for us
	wesClient = DNAStackWESClient('~/.keys/DNAStackWESkey.json')
	
	faspRunner.configure(searchClient, drsClient, wesClient)
		
	faspRunner.runQuery(query, 'One k query using Search and WES')
    
if __name__ == "__main__":
    main(sys.argv[1:])
    


	
	

	
	









