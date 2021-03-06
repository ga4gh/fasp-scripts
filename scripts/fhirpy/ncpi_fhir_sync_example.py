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
	
    # Search for patients
	resources = client.resources('Patient')  
	resources = resources.search(gender='female').limit(10)
	patients = resources.fetch()
	print("# of patients:{}".format(len(patients)))
	#for p in patients:
	#	print(p)


main()

