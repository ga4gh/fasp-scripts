import asyncio
import os
import json
from fhirpy import AsyncFHIRClient


async def main():
	
	endpoint = 'https://ncpi-api-fhir-service-dev.kidsfirstdrc.org'
	full_cookie_path = os.path.expanduser('~/.keys/kf_cookies.json')
	print(full_cookie_path)
	with open(full_cookie_path) as f:
			cookies = json.load(f)
			
	# Create an instance
	client = AsyncFHIRClient(
        endpoint,
        extra_headers=cookies
    )

    # Search for patients
	resources = client.resources('Patient')  # Return lazy search set
	resources = resources.search(name='John').limit(10).sort('name')
	patients = await resources.fetch()  # Returns list of AsyncFHIRResource
	

	print("# of patients:{}".format(len(patients)))





