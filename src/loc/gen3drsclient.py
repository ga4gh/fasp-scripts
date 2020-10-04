import requests
import json
import os.path

from loc import DRSClient


class Gen3DRSClient(DRSClient):
    '''Handles Gen3 specific authentication using Fence'''
    
    # Initialize a DRS Client for the service at the specified url base
    # and with the REST resource to provide an access key 
    def __init__(self, api_url_base,  access_token_resource_path, api_key_path,
    access_id=None):
        super().__init__(api_url_base, access_id)
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
    def __init__(self, api_key_path,  access_id=None):
        super().__init__('https://nci-crdc.datacommons.io', '/user/credentials/api/access_token',
            api_key_path, access_id)

class bdcDRSClient(Gen3DRSClient):
    
    # Mostly done by the Gen3DRSClient, this just deals with url and end point specifics
    def __init__(self, api_key_path, access_id=None):
        super().__init__('https://gen3.biodatacatalyst.nhlbi.nih.gov', '/user/credentials/cdis/access_token',
            api_key_path, access_id)


if __name__ == "__main__":
    print ('______________________________________')
    print ('BDC')
    bdcClient = bdcDRSClient('~/.keys/BDCcredentials.json', 'gs')
    id = 'dg.4503/dbd55e76-1100-40b3-b420-0eaeee478fbc'
    res = bdcClient.getObject(id)
    print('GetObject')
    print (res)
    print('URL')
    url = bdcClient.getAccessURL(id)
    print (url)
    print ('______________________________________')
    print ('CRDC')
    crdcClient = crdcDRSClient('~/.keys/CRDCAPIKey.json', 's3')
    id = 'f360253c-d7d7-47cb-947a-b26e0b41b800'
    res = crdcClient.getObject(id)
    print('GetObject')
    print (res)
    print('URL')
    url = crdcClient.getAccessURL(id)
    print (url)
           
