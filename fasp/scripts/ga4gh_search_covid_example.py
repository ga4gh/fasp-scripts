#  IMPORTS
import sys 



from fasp.search  import DiscoverySearchClient




def main(argv):

	# Step 1 - Discovery
	# query for relevant DRS objects
	
	searchClient = DiscoverySearchClient('https://search-presto-public-covid19.prod.dnastack.com/')
	
	# List tables
	#searchClient.listTables()
	
	# List table schema
	#searchClient.listTableInfo('coronavirus_dnastack_curated.covid_cloud_production.sequences')
	
	
	query = 'select accession, biosample, genus, species from coronavirus_dnastack_curated.covid_cloud_production.sequences limit 10'
	res = searchClient.runQuery(query)
	print(res)
	

if __name__ == "__main__":
	main(sys.argv[1:])