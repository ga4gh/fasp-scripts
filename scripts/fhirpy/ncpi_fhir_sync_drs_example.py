from fhirpy import SyncFHIRClient
import os
import json


def main():
	
	endpoint = 'https://ncpi-api-fhir-service-dev.kidsfirstdrc.org'
	full_cookie_path = os.path.expanduser('~/.keys/kf_cookies.json')
	print(full_cookie_path)
	with open(full_cookie_path) as f:
			cookies = json.load(f)

	client = SyncFHIRClient(endpoint, extra_headers=cookies)
	
		
	document_references = client.resources("DocumentReference")
	document_references.search(_profile='http://fhir.ncpi-project-forge.io/StructureDefinition/ncpi-drs-document-reference')
	drs_ids = document_references.fetch()
	print("# of ids:{}".format(len(drs_ids)))
	for d in drs_ids:
		print(d['content'][0]['attachment']['url'])

	


main()
