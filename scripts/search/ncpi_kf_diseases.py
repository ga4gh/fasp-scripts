''' Basic query on NCPI FHIR server Patient resource via DNAStack Search test implementation'''
#  IMPORTS
import sys
import json
import pandas as pd


from fasp.search  import DataConnectClient




def main(argv):

	searchClient = DataConnectClient('https://publisher-data.publisher.dnastack.com/data-connect/')

	query = """
		SELECT
			json_extract_scalar(ncpi_disease, '$.code.coding[0].code') AS code,
			json_extract_scalar(ncpi_disease, '$.code.text') AS text
		FROM collections.public_datasets.public_ncpi_disease
		ORDER BY code
	"""
	res = searchClient.runQuery(query)

	diseases = { row['code']: row['text'] for row in res }
	disease_df = pd.DataFrame.from_dict(diseases, orient='index', columns=[ 'Term'])

	for k,v in diseases.items():
		print(k,v)

	print("found {} disease records".format(len(res)))
	print("There were {} disease codes used".format(len(diseases)))

	disease_df.to_csv('~/ncpi_kf_disease_terms.tsv', sep = '\t')

if __name__ == "__main__":
	main(sys.argv[1:])