import requests
import json

class DRSClient:
    
	# Initialize a DRS Client for the service at the specified url base
	# and with the REST resource to provide an access key 
	def __init__(self, api_url_base, access_id=None, debug=False):
		self.api_url_base = api_url_base
		self.access_id = access_id
		self.id = None
		self.name = None
		self.version = None
		self.debug = debug

	@classmethod
	def fromRegistryEntry(cls, registryEntry):
		instance = cls(registryEntry['url'])
		instance.id = registryEntry['id']
		instance.name = registryEntry['name']
		instance.version = registryEntry['version']
		return instance
			

    # Get info about a DrsObject
    # See https://ga4gh.github.io/data-repository-service-schemas/preview/develop/docs/#_getobject
	def getObject(self, object_id):
		api_url = '{0}/ga4gh/drs/v1/objects/{1}'.format(self.api_url_base, object_id)
		if self.debug:
			print(api_url)
		# headers generated error on SRA, doesn't seem to be required by the others
		#headers = {'Content-Type': 'application/json'}
		#response = requests.get(api_url, headers=headers)
		response = requests.get(api_url)
		if response.status_code == 200:
			resp = response.content.decode('utf-8')
			return json.loads(resp)
		else:
			print(response.content.decode('utf-8'))
			return response.status_code

	# Get a URL for fetching bytes. 
	# See https://ga4gh.github.io/data-repository-service-schemas/preview/develop/docs/#_getaccessurl
	def getAccessURL(self, object_id, access_id=None):
		if access_id == None:
			access_id = self.access_id
		headers = {'Content-Type': 'application/json',
		'Authorization': 'Bearer {0}'.format(self.access_token)}
		api_url = '{0}/ga4gh/drs/v1/objects/{1}/access/{2}'.format(self.api_url_base, object_id, access_id)
		response = requests.get(api_url, headers=headers)
		if response.status_code == 200:
			resp = response.content.decode('utf-8')
			return json.loads(resp)['url']
		if response.status_code == 401:
			return None
		else:
			print (response)
			return None