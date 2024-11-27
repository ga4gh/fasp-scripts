#  IMPORTS
import sys



from fasp.search  import DataConnectClient




def main(argv):

	# Step 1 - Discovery
	# query for relevant DRS objects

	searchClient = DataConnectClient('https://publisher-data.publisher.dnastack.com/data-connect')

	# List tables
	#searchClient.listTables()

	# List table schema
	#searchClient.listTableInfo('coronavirus_dnastack_curated.covid_cloud_production.sequences')


	query = 'select accession, biosample, genus, species from coronavirus_dnastack_curated.covid_cloud_production.sequences limit 10'
	res = searchClient.runQuery(query, returnType='dataframe')
	print(res)


if __name__ == "__main__":
	main(sys.argv[1:])