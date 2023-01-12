''' Simple example query within a FHIR resource. Query on id'''
#  IMPORTS
import sys
import json


from fasp.search  import DataConnectClient




def main(argv):

	# Step 1 - Discovery
	# query for relevant DRS objects

	searchClient = DataConnectClient('https://data.publisher.dnastack.com/data-connect/')

	# List tables
	#searchClient.listTables()

	# List table schema
	#searchClient.listTableInfo('coronavirus_dnastack_curated.covid_cloud_production.sequences')


	query = """select id, patient from collections.public_datasets.public_patient
	where json_extract_scalar(patient, '$.id') = '451133' limit 3"""



	res = searchClient.runQuery(query)

	print(json.dumps(res, indent=2))



if __name__ == "__main__":
	main(sys.argv[1:])