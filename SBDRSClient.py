import requests
import json
import os.path

from DRSClient import DRSClient


class SBDRSClient(DRSClient):
    
    # Initialize a DRS Client for the service at the specified url base
    # and with the REST resource to provide an access key 
	def __init__(self, api_url_base, api_key_path, instance):
		super().__init__(api_url_base)
		full_key_path = os.path.expanduser(api_key_path)
		with open(full_key_path) as f:
			auth_content = json.load(f)
		self.auth_token = auth_content[instance]['auth_token']

			

    # Get info about a DrsObject
    # See https://ga4gh.github.io/data-repository-service-schemas/preview/develop/docs/#_getobject
	def getObject(self, object_id):
		headers = {'Content-Type': 'application/json',
		'Authorization': 'Bearer {0}'.format(self.auth_token)}
		api_url = '{0}/ga4gh/drs/v1/objects/{1}'.format(self.api_url_base, object_id)
		response = requests.get(api_url, headers=headers)
		if response.status_code == 200:
			resp = response.content.decode('utf-8')
			return json.loads(resp)
		else:
			return None
    	    
    # Get a URL for fetching bytes. 
    # See https://ga4gh.github.io/data-repository-service-schemas/preview/develop/docs/#_getaccessurl
#     def getAccessURL(self, object_id, access_id):
#          auth_token = self.auth_token['auth_token']
#          headers = {'Content-Type': 'application/json',
#          'Authorization': 'Bearer {0}'.format(auth_token)}
#          api_url = '{0}/ga4gh/drs/v1/objects/{1}/access/{2}'.format(self.api_url_base, object_id, access_id)
#          response = requests.get(api_url, headers=headers)
#          if response.status_code == 200:
#             resp = response.content.decode('utf-8')
#             return json.loads(resp)['url']
#          else:
#             print (response)
#             return None

class sbcgcDRSClient(SBDRSClient):
    
    # Mostly done by the SBDRSClient, this just deals with url and end point specifics
    def __init__(self, api_key_path):
    	super().__init__('https://cgc-ga4gh-api.sbgenomics.com', api_key_path, 'cgc')

class cavaticaDRSClient(SBDRSClient):
    
    # Mostly done by the SBDRSClient, this just deals with url and end point specifics
    def __init__(self, api_key_path):
    	super().__init__('https://cavatica-ga4gh-api.sbgenomics.com', api_key_path, 'cavatica')



if __name__ == "__main__":
	print ("Cancer Genomics Cloud")
	sbClient = sbcgcDRSClient('~/.keys/sevenbridges_keys.json')
	res = sbClient.getObject('5baa9d00e4b0abc1388b8ce0')
	print (res)
	print ("______________________")
	print ("Cavatica")
	sbClient = cavaticaDRSClient('~/.keys/sevenbridges_keys.json')
	res = sbClient.getObject('578cf947507c17681a3117d1')
	print (res)

           
