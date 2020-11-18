''' Basic query on NCPI FHIR server Patient resource via DNAStack Search test implementation'''
#  IMPORTS
import sys 
import json
import pandas as pd


from fasp.search  import DiscoverySearchClient




def main(argv):

	searchClient = DiscoverySearchClient('https://ga4gh-search-adapter-presto-public.prod.dnastack.com')
	
	query = 'select id, disease from kidsfirst.ga4gh_tables.ncpi_disease'
	res = searchClient.runQuery(query)

	diseases = {}
	for r in res:
		disease = r[1]
		dName = disease['identifier'][0]['value']
		code = disease['code']['coding'][0]['code']
		text = disease['code']['text']
		diseases[code] = text

	disease_df = pd.DataFrame.from_dict(diseases, orient='index', columns=[ 'Term'])
	

	for k,v in diseases.items():
		print(k,v)

		
	print("found {} disease records".format(len(res)))
	print("There were {} disease codes used".format(len(diseases)))
	
	disease_df.to_csv('~/ncpi_kf_disease_terms.tsv', sep = '\t')
	
if __name__ == "__main__":
	main(sys.argv[1:])