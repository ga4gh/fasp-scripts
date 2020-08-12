import requests
import json
import os.path


class Gen3DRSClient:

    
    # Initialize a DRS Client for the service at the specified url base
    # and with the REST resource to provide an access key 
    def __init__(self, api_url_base,  access_token_resource_path, api_key_path):
    	self.api_url_base = api_url_base
    	self.access_token_resource_path = access_token_resource_path
    	full_key_path = os.path.expanduser(api_key_path)
    	with open(full_key_path) as f:
    		self.api_key = json.load(f)
    	self.updateAccessToken()
			

    # Obtain an access_token using the provided Fence API key.
    # The client object will retain the access key for subsequent calls
    def updateAccessToken(self):
        headers = {'Content-Type': 'application/json'}
        api_url = '{0}{1}'.format(self.api_url_base, self.access_token_resource_path)
        response = requests.post(api_url, headers=headers, json=self.api_key)

        if response.status_code == 200:
            #access_token['access_token']
            self.access_token = response.content.decode('utf-8')
            return json.loads(self.access_token)
        else:
            return None
        
    # Get info about a DrsObject
    # See https://ga4gh.github.io/data-repository-service-schemas/preview/develop/docs/#_getobject
    def getObject(self, object_id):
         headers = {'Content-Type': 'application/json'}
         api_url = '{0}/ga4gh/drs/v1/objects/{1}'.format(self.api_url_base, object_id)
         response = requests.get(api_url, headers=headers)
         if response.status_code == 200:
            resp = response.content.decode('utf-8')
            return json.loads(resp)
         else:
            return None
    	    
    # Get a URL for fetching bytes. 
    # See https://ga4gh.github.io/data-repository-service-schemas/preview/develop/docs/#_getaccessurl
    def getAccessURL(self, object_id, access_id):
         access_token = json.loads(self.access_token)
         headers = {'Content-Type': 'application/json',
         'Authorization': 'Bearer {0}'.format(access_token['access_token'])}
         api_url = '{0}/ga4gh/drs/v1/objects/{1}/access/{2}'.format(self.api_url_base, object_id, access_id)
         response = requests.get(api_url, headers=headers)
         if response.status_code == 200:
            resp = response.content.decode('utf-8')
            return json.loads(resp)['url']
         else:
            print (response)
            return None



           
