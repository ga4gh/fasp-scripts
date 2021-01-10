import requests
import json
import sys
''' base class for a WES Client'''
class WESClient:

    
	def __init__(self, api_url_base):
		self.api_url_base = api_url_base


	def getTaskStatus(self, run_id, verbose=False):
		runURL = "{}/{}".format(self.api_url_base, run_id)
		if verbose: print("Get request sent to: {}".format(runURL))
		runResp = requests.get(runURL, headers=self.headers)
		if runResp.status_code == 200:
			run = runResp.json()
			if verbose: print(json.dumps(run, indent=2))
			return run['state']
		if runResp.status_code == 400:
			return 'task not found'
		print(runResp)
		
	def runWorkflow(self, body, verbose=False):
		if verbose: print("sending to {}".format( self.api_url_base))
		
		headers = self.headers
		headers['Content-Type'] = 'application/json'
		response = requests.post(self.api_url_base, headers=headers, data = json.dumps(body).encode('utf-8'))
		if verbose:
			print(response.text)
			print(response)
		if response.status_code == 200:
			return response.json()['run_id']
		elif response.status_code == 401:
			print("WES server authentication failed")
			sys.exit(1)
		else:
			print("WES run submission failed. Response status:{}".format(response.status_code))
			sys.exit(1)
		
