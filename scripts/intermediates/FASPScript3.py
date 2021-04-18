#  IMPORTS
import sys 

from fasp.runner import FASPRunner

# The implementations we're using
from fasp.loc import bdcDRSClient
from fasp.workflow import GCPLSsamtools
from fasp.search import DataConnectClient

def main(argv):


	faspRunner = FASPRunner(pauseSecs=0)
	settings =faspRunner.settings
	# Step 1 - Discovery
	# query for relevant DRS objects
	searchClient = DataConnectClient('https://ga4gh-search-adapter-presto-public.prod.dnastack.com/')
	query = "select submitter_id, read_drs_id drsid from thousand_genomes.onek_genomes.ssd_drs where population = 'BEB' limit 3"

	# Step 2 - DRS - set up a DRS Client
	# CRDC
	drsClient = bdcDRSClient('~/.keys/bdc_credentials.json', 'gs')

	
	# Step 3 - set up a class that runs samtools for us
	# providing the location where we the results to go
	location = 'projects/{}/locations/{}'.format(settings['GCPProject'], settings['GCPPipelineRegion'])
	mysam = GCPLSsamtools(location, settings['GCPOutputBucket'])	

	faspRunner.configure(searchClient, drsClient, mysam)
		
	faspRunner.runQuery(query, 'One k query using Search')
	    
if __name__ == "__main__":
    main(sys.argv[1:])
    


	
	

	
	









