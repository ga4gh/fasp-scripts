''' Simple example query within a FHIR resource. Query on id'''
#  IMPORTS
import sys 
import json


from fasp.search  import DiscoverySearchClient




def main(argv):

	# Step 1 - Discovery
	# query for relevant DRS objects
	
	searchClient = DiscoverySearchClient('https://ga4gh-search-adapter-presto-public.prod.dnastack.com')
	
	# List tables
	#searchClient.listTables()
	
	# List table schema
	#searchClient.listTableInfo('coronavirus_dnastack_curated.covid_cloud_production.sequences')
	
	
	query = """select id, patient from kidsfirst.ga4gh_tables.patient 
	where json_extract_scalar(patient, '$.id') = '451133' limit 3"""
	
	
	
	res = searchClient.runQuery(query)

	print(json.dumps(res, indent=2))

	

if __name__ == "__main__":
	main(sys.argv[1:])