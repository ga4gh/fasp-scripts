''' Query on gender (uncoded) '''
#  IMPORTS
import sys
import json


from fasp.search  import DataConnectClient




def main(argv):

	searchClient = DataConnectClient('https://publisher-data.publisher.dnastack.com/data-connect/')

	query = """select id, patient from collections.public_datasets.public_patient
	where json_extract_scalar(patient, '$.gender') = 'female'
	limit 3"""

	showDetail = True

	res = searchClient.runQuery(query)

	if showDetail:
		print(json.dumps(res, indent=2))

	for r in res:
		patient = r[1]
		print(patient['id'], patient['gender'])



if __name__ == "__main__":
	main(sys.argv[1:])