''' Query on gender (uncoded) '''
#  IMPORTS
import sys
import json


from fasp.search  import DataConnectClient




def main(argv):

	searchClient = DataConnectClient('https://data.publisher.dnastack.com/data-connect/')

	query = """select id, patient from collections.public_datasets.public_patient
	where json_extract_scalar(patient, '$.extension[0].url') = 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity'
	limit 3"""
	#TODO query on the value of ethnicity

	showDetail = True

	res = searchClient.runQuery(query)

	if showDetail:
		print(json.dumps(res, indent=2))

	for r in res:
		patient = r[1]
		print(patient['id'], patient['gender'])
		for e in patient['extension']:
			print (e['url'])
			print(e['extension'][0]['url'])
			vc = e['extension'][0]['valueCoding']
			print(vc['code'], vc['display'])



if __name__ == "__main__":
	main(sys.argv[1:])