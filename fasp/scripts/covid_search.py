#  IMPORTS
import sys 



from fasp.search  import DiscoverySearchClient




def main(argv):

	# Step 1 - Discovery
	# query for relevant DRS objects
	
	searchClient = DiscoverySearchClient('https://search-presto-public-covid19.prod.dnastack.com')
	
	# List tables
	tList = searchClient.listTables(verbose=False)
	
	# List table schema
	for t in tList:
		res = searchClient.listTableInfo(t, verbose=False)
		print(t)
		if 'data_model' in res:
			print(res['data_model']['description'])
		else:
			print('No data model')
	
	
	
	#query = 'select accession, biosample, genus, species from coronavirus_dnastack_curated.covid_cloud_production.sequences limit 10'
	#res = searchClient.runQuery(query, returnType='dataframe')
	#print(res)
	

if __name__ == "__main__":
	main(sys.argv[1:])