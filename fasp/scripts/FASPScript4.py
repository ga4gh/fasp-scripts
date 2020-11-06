#  IMPORTS
import sys 



from fasp.search import DiscoverySearchClient


def main(argv):

	# Step 1 - Discovery
	# query for relevant DRS objects
	searchClient = DiscoverySearchClient('https://ga4gh-search-adapter-presto-public.prod.dnastack.com/')
	query = "select submitter_id, read_drs_id drsid from thousand_genomes.onek_genomes.ssd_drs where population = 'ACB' limit 3"
	
		
	res = searchClient.runQuery(query)
	
	print(res)
    
if __name__ == "__main__":
    main(sys.argv[1:])
    


	
	

	
	









