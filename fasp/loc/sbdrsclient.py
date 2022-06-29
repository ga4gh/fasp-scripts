'''
'A DRS client for Seven Bridges DRS services. Handles SB specific authentication.
'''

import json
import os.path
import requests

from fasp.loc import DRSClient


class SBDRSClient(DRSClient):

    # Initialize a DRS Client for the service at the specified url base
    # and with the REST resource to provide an access key 
	def __init__(self, api_url_base, api_key_path, access_id, debug=False):
		super().__init__(api_url_base, access_id, debug=debug)
		self.api_key_path = api_key_path


	def authorize(self):
		full_key_path = os.path.expanduser(self.api_key_path)
		with open(full_key_path) as f:
			auth_content = json.load(f)
		self.auth_token = auth_content['auth_token']
		self.authorized = True

    # Need to override this method as Get object requires auth on Seven Bridges services
    # Get info about a DrsObject
    # See https://ga4gh.github.io/data-repository-service-schemas/preview/develop/docs/#_getobject
	def get_object(self, object_id):
		if not self.authorized:
			self.authorize()

		headers = self.getHeaders()
		
		headers['Content-Type'] = 'application/json'

		api_url = '{0}/ga4gh/drs/v1/objects/{1}'.format(self.api_url_base, object_id)
		response = requests.get(api_url, headers=headers)
		if response.status_code == 200:
			resp = response.content.decode('utf-8')
			return json.loads(resp)
		else:
			print (response.raise_for_status())
			return None

	def get_access_url(self, object_id, access_id=None):
		if not self.authorized:
			self.authorize()
		return DRSClient.get_access_url(self, object_id, access_id=access_id)

	def getHeaders(self): 
		return {'X-SBG-Auth-Token' : self.auth_token }


class sbcgcDRSClient(SBDRSClient):
    '''client for Cancer Genomics Cloud Seven Bridges DRS server'''
    
    # Mostly done by the SBDRSClient, this just deals with url and end point specifics
    def __init__(self, api_key_path, access_id, debug=False):
    	super().__init__('https://cgc-ga4gh-api.sbgenomics.com', api_key_path, access_id, debug=debug)

class cavaticaDRSClient(SBDRSClient):
    '''client for Cavatica Seven Bridges DRS Server'''    
    # init mostly done by the SBDRSClient, this just deals with url and end point specifics
    def __init__(self, api_key_path, access_id, debug=False):
    	super().__init__('https://cavatica-ga4gh-api.sbgenomics.com', api_key_path, access_id, debug=debug)

class sbbdcDRSClient(SBDRSClient):
    '''client for BioDataCatalyst Seven Bridges DRS Server'''    
    # init mostly done by the SBDRSClient, this just deals with url and end point specifics
    def __init__(self, api_key_path, access_id, debug=False):
    	super().__init__('https://ga4gh-api.sb.biodatacatalyst.nhlbi.nih.gov', api_key_path, access_id, debug=debug)



if __name__ == "__main__":
	print ("Cancer Genomics Cloud")
	sbClient = sbcgcDRSClient('~/.keys/sbcgc_key.json', 's3')
	#res = sbClient.get_object('5bb22646e4b0db6385b3a119')
	#res = sbClient.get_object('5ba0025ce4b0f7470b2289bc')
	res = sbClient.get_object('5ba0025ce4b0f7470b228a9a')
	#res = sbClient.get_access_url('5ba0025ce4b0f7470b2289bc')
	print(res)
	# Thousand Genomes meta csv file - no guarantee this will be there in future!
	#res = sbClient.get_object('5f404097e4b0bf4ad1323012')

	print ("______________________")
	print ("Cavatica")
	sbClient = cavaticaDRSClient('~/.keys/sbcav_key.json', 'gs')
	res = sbClient.get_object('578cf947507c17681a3117d1')

	print (res)

           
