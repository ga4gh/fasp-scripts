from fhirpy import SyncFHIRClient


def main():
	
	endpoint = 'https://ncpi-api-fhir-service-dev.kidsfirstdrc.org'
	# Create an instance
	client = SyncFHIRClient(endpoint)

	
    # Search for patients
	resources = client.resources('Patient')  
	resources = resources.search(gender='female').limit(1000)
	patients = resources.fetch()
	print("# of patients:{}".format(len(patients)))


main()

