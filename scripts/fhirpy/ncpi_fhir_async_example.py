import asyncio
from fhirpy import AsyncFHIRClient


async def main():
	
	endpoint = 'https://ncpi-api-fhir-service-dev.kidsfirstdrc.org'
	# Create an instance
	client = AsyncFHIRClient(
        endpoint,
        authorization='Bearer TOKEN',
    )

    # Search for patients
	resources = client.resources('Patient')  # Return lazy search set
	resources = resources.search(name='John').limit(10).sort('name')
	patients = await resources.fetch()  # Returns list of AsyncFHIRResource
	

	print("# of patients:{}".format(len(patients)))





