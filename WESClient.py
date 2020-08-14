import requests

class WESClient:

    
    def __init__(self, api_url_base,  access_token_path):
    	self.api_url_base = api_url_base
    	full_key_path = os.path.expanduser(access_token_path)
    	with open(full_key_path) as f:
    		self.accessToken = json.load(f)

	def runWorkflow()
		payload = {'workflow_url': 'checksum.wdl'}
		files = [
			('workflow_params', open('../wes/inputs.json','rb')),
			('workflow_attachment', open('../wes/checksum.wdl','rb'))
		]
		headers = {
  			'Authorization': 'Bearer ',
  			'Cookie': 'JSESSIONID=CA641A6F3C5CD587909E3A9B9B9C5C3C'
		}

		response = requests.request("POST", self.api_url_base, headers=headers, data = payload, files = files)

		print(response.text.encode('utf8'))
		
if __name__ == "__main__":
	myClient = DiscoverySearchClient('https://ddap-wes-service.prod.dnastack.com/ga4gh/wes/v1/runs', '~/.keys/DNAStackWESkey.json')

	res = myClient.runWorkflow()
	print (res)
