import requests
import json
import os.path

from fasp.loc import DRSClient
#from fasp.examples.discoverySearch.getFirstModel import result


class Gen3DRSClient(DRSClient):
    '''Handles Gen3 specific authentication using Fence'''
    
    # Initialize a DRS Client for the service at the specified url base
    # and with the REST resource to provide an access key 
    def __init__(self, api_url_base,  access_token_resource_path, api_key_path,
    access_id=None, debug=False):
        super().__init__(api_url_base, access_id, debug=debug)
        self.access_token_resource_path = access_token_resource_path
        full_key_path = os.path.expanduser(api_key_path)
        with open(full_key_path) as f:
            self.api_key = json.load(f)
        code = self.updateAccessToken()
        if code == 401:
            print('Invalid access token in {}'.format(full_key_path))
        elif code != 200:
            print('Error {} getting Access token for {}'.format(code, api_url_base))
            print('Using {}'.format(full_key_path))


    # Obtain an access_token using the provided Fence API key.
    # The client object will retain the access key for subsequent calls
    def updateAccessToken(self):
        headers = {'Content-Type': 'application/json'}
        api_url = '{0}{1}'.format(self.api_url_base, self.access_token_resource_path)
        response = requests.post(api_url, headers=headers, json=self.api_key)

        if response.status_code == 200:
            resp = json.loads(response.content.decode('utf-8'))
            self.access_token = resp['access_token']
        return response.status_code
        


class crdcDRSClient(Gen3DRSClient):
    
    # Mostly done by the Gen3DRSClient, this just deals with url and end point specifics
    def __init__(self, api_key_path=None,  access_id=None,  debug=False):
        if api_key_path == None:
            api_key_path='~/.keys/crdc_credentials.json'
        self.file_endpt = 'https://api.gdc.cancer.gov/files/'
        super().__init__('https://nci-crdc.datacommons.io', '/user/credentials/api/access_token',
            api_key_path, access_id, debug)
        
    def getFileData(self, file_id, expanded=False, linked=False):
        headers = {'Content-Type': 'application/json'}

        fields = [
		"file_name",
		"data_format",
		"platform",
		"access",
		"created_datetime",
		"data_category",
		"data_type",
		"experimental_strategy",
		"file_size",
		"origin",
		"revision",
		"type",
		]

        if linked or expanded:
            fields += [
			"cases.case_id",
			"file_name",
			"data_format",
			"platform",
			"metadata_files.file_id",
			"metadata_files.file_name",
			"analysis.analysis_id",
			"annotations.annotation_id",
			"archive.archive_id",
			"associated_entities.entity_id",
			"associated_entities.entity_type",
			"center.center_id",
			"metadata_files.file_id",
			"index_files.file_id",
			"downstream_analyses.analysis_id"
			]

        if linked:
            fields += [
			"cases.project.disease_type",
			"cases.demographic.race",
			"cases.demographic.state",
			"cases.demographic.submitter_id",
			"cases.demographic.updated_datetime",
			"cases.demographic.year_of_birth",
			"cases.demographic.year_of_death",
			"cases.diagnoses.age_at_diagnosis",
			"cases.diagnoses.classification_of_tumor",
			"cases.diagnoses.created_datetime",
			"cases.diagnoses.days_to_last_known_disease_status",
			"cases.diagnoses.days_to_recurrence",
			"cases.diagnoses.morphology",
			"cases.diagnoses.primary_diagnosis",
			"cases.diagnoses.prior_malignancy",
			"cases.diagnoses.progression_or_recurrence",
			"cases.diagnoses.site_of_resection_or_biopsy",
			"cases.diagnoses.tissue_or_organ_of_origin",
			"cases.diagnoses.tumor_grade",
			"cases.diagnoses.tumor_stage"
			]

        fields = ",".join(fields)

        body = {
			"filters":{
						"op":"=",
						"content":{
							"field":"file_id",
							"value":file_id
						}
				
			},
			"fields":fields,
			"format":"json",
		}

        resp = requests.post(self.file_endpt, data=json.dumps(body), headers=headers)
        return resp.json()['data']['hits'][0]

class bdcDRSClient(Gen3DRSClient):
    
    # Mostly done by the Gen3DRSClient, this just deals with url and end point specifics
    def __init__(self, api_key_path, access_id=None,  debug=False):
        super().__init__('https://gen3.biodatacatalyst.nhlbi.nih.gov', '/user/credentials/cdis/access_token',
            api_key_path, access_id, debug)

class kfDRSClient(Gen3DRSClient):
    
    # Mostly done by the Gen3DRSClient, this just deals with url and end point specifics
    def __init__(self, api_key_path, access_id=None,  debug=False):
        super().__init__('https://data.kidsfirstdrc.org', '/user/credentials/cdis/access_token',
            api_key_path, access_id, debug)

class anvilDRSClient(Gen3DRSClient):
	
	
	def __init__(self, api_key_path, userProject=None, access_id=None,  debug=False):
		self.userProject = userProject
		super().__init__('https://gen3.theanvil.io','/user/credentials/api/access_token', api_key_path, access_id, debug)

	# Get a URL for fetching bytes. 
	# Anvil GCP resources requires you to provide the userAccount to which charges will be accrued
	# That user account must grant serviceusage.services.use access to your anvil service account
	# e.g. to user-123@anvilprod.iam.gserviceaccount.com
	def getAccessURL(self, object_id, access_id=None):
		result = super().getAccessURL(object_id, access_id)

		if result != None:
			if self.userProject == None:
				return result
			else:
				return '{}&userProject={}'.format(result, self.userProject)
		else:
			return None

if __name__ == "__main__":
    print ('______________________________________')
    print ('BDC')
    bdcClient = bdcDRSClient('~/.keys/bdc_credentials.json', 'gs')
    id = 'dg.4503/dbd55e76-1100-40b3-b420-0eaeee478fbc'
    res = bdcClient.getObject(id)
    print('GetObject')
    print (res)
    print('URL')
    url = bdcClient.getAccessURL(id)
    print (url)
    print ('______________________________________')
    print ('CRDC')
    crdcClient = crdcDRSClient('~/.keys/crdc_credentials.json', 's3')
    id = 'f360253c-d7d7-47cb-947a-b26e0b41b800'
    res = crdcClient.getObject(id)
    print('GetObject')
    print (res)
    print('URL')
    url = crdcClient.getAccessURL(id)
    print (url)
           
