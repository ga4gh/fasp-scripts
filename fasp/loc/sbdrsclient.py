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
	def __init__(self, api_url_base, api_key_path, instance, access_id, debug=False):
		super().__init__(api_url_base, access_id, debug=debug)
		full_key_path = os.path.expanduser(api_key_path)
		with open(full_key_path) as f:
			auth_content = json.load(f)
		self.access_token = auth_content[instance]['auth_token']

    # Need to override this method as Get object requires auth on Seven Bridges services
    # Get info about a DrsObject
    # See https://ga4gh.github.io/data-repository-service-schemas/preview/develop/docs/#_getobject
	def getObject(self, object_id):
		headers = self.getHeaders()
		headers['Content-Type'] = 'application/json'

		api_url = '{0}/ga4gh/drs/v1/objects/{1}'.format(self.api_url_base, object_id)
		response = requests.get(api_url, headers=headers)
		if response.status_code == 200:
			resp = response.content.decode('utf-8')
			return json.loads(resp)
		else:
			return response.status_code

	def getHeaders(self): 
		return {'X-SBG-Auth-Token' : self.access_token }


class sbcgcDRSClient(SBDRSClient):
    '''client for Cancer Genomics Cloud Seven Bridges DRS server'''
    
    # Mostly done by the SBDRSClient, this just deals with url and end point specifics
    def __init__(self, api_key_path, access_id, debug=False):
    	super().__init__('https://cgc-ga4gh-api.sbgenomics.com', api_key_path, 'cgc', access_id, debug=debug)

class cavaticaDRSClient(SBDRSClient):
    '''client for Cavatica Seven Bridges DRS Server'''    
    # init mostly done by the SBDRSClient, this just deals with url and end point specifics
    def __init__(self, api_key_path, access_id, debug=False):
    	super().__init__('https://cavatica-ga4gh-api.sbgenomics.com', api_key_path, 'cavatica', access_id, debug=debug)

class sbbdcDRSClient(SBDRSClient):
    '''client for BioDataCatalyst Seven Bridges DRS Server'''    
    # init mostly done by the SBDRSClient, this just deals with url and end point specifics
    def __init__(self, api_key_path, access_id, debug=False):
    	super().__init__('https://ga4gh-api.sb.biodatacatalyst.nhlbi.nih.gov', api_key_path, 'bdc', access_id, debug=debug)



if __name__ == "__main__":
	print ("Cancer Genomics Cloud")
	sbClient = sbcgcDRSClient('~/.keys/sevenbridges_keys.json', 's3')
	#res = sbClient.getObject('5bb22646e4b0db6385b3a119')
	#res = sbClient.getObject('5ba0025ce4b0f7470b2289bc')
	res = sbClient.getObject('5ba0025ce4b0f7470b228a9a')
	#res = sbClient.getAccessURL('5ba0025ce4b0f7470b2289bc')
	print(res)
	# Thousand Genomes meta csv file - no guarantee this will be there in future!
	#res = sbClient.getObject('5f404097e4b0bf4ad1323012')

	print ("______________________")
	print ("Cavatica")
	sbClient = cavaticaDRSClient('~/.keys/sevenbridges_keys.json', 'gs')
	res = sbClient.getObject('578cf947507c17681a3117d1')

	print (res)

           
