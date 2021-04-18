''' Basic query on NCPI FHIR server Patient resource via DNAStack Search test implementation'''
#  IMPORTS
import sys 
import json


from fasp.search  import DataConnectClient




def main(argv):

	searchClient = DataConnectClient('https://ga4gh-search-adapter-presto-public.prod.dnastack.com')

	
	
	query = 'select id, patient from kidsfirst.ga4gh_tables.patient limit 3'
	res = searchClient.runQuery(query)

	print(json.dumps(res, indent=2))

	

if __name__ == "__main__":
	main(sys.argv[1:])