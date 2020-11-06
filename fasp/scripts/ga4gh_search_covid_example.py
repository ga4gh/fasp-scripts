#  IMPORTS
import sys 



from fasp.search  import DiscoverySearchClient




def main(argv):

	# Step 1 - Discovery
	# query for relevant DRS objects
	
	searchClient = DiscoverySearchClient('https://search-presto-public-covid19.prod.dnastack.com')
	
	# List table 
	searchClient.listTables()
	
	#query = ""
		
	#res = searchClient.runQuery(query)
	

    
if __name__ == "__main__":
    main(sys.argv[1:])