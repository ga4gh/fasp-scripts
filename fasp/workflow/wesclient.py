import json
from typing import Dict, Optional, Union, IO

import requests

''' base class for a WES Client'''
class WESClient:
	api_url_base: str
	headers: Dict[str, str]


	def __init__(self, api_url_base):
		self.api_url_base = api_url_base
		self.headers = {}

	@classmethod
	def _fromRegistryEntry(cls, registryEntry):
		instance = cls(registryEntry['url'])
		return instance

	@classmethod
	def fromRegistryByID(cls, regID):
		'''Get a WES service from details in the GA4GH Registry. 
		Note: Currently this method has limited utility as it does not yet address how authentication would be passed to the client'''
		url ='https://registry.ga4gh.org/v1/services/{}'.format(regID)
		regEntry = requests.get(url)
		instance = cls._fromRegistryEntry(json.loads(regEntry.content))
		return instance

	def getTaskStatus(self, run_id, verbose=False):
		runURL = "{}/runs/{}".format(self.api_url_base, run_id)
		if verbose: print("Get request sent to: {}".format(runURL))
		runResp = requests.get(runURL, headers=self.headers)
		if runResp.status_code == 200:
			run = runResp.json()
			if verbose: print(json.dumps(run, indent=2))
			return run['state']
		if runResp.status_code == 400:
			return 'task not found'
		print(runResp)
		
	def GetRunLog(self, run_id, verbose=False):
		runURL = "{}/runs/{}".format(self.api_url_base, run_id)
		if verbose: print("Get request sent to: {}".format(runURL))
		runResp = requests.get(runURL, headers=self.headers)
		if runResp.status_code == 200:
			run = runResp.json()
			if verbose: print(json.dumps(run, indent=2))
			return run
		if runResp.status_code == 400:
			return 'task not found'
		print(runResp)

	def runGenericWorkflow(
			self,
			workflow_url: str,
			workflow_params: Union[str, IO[bytes], None] = None,
			workflow_engine_params: Union[str, IO[bytes], None] = None,
			workflow_type: Optional[str] = None,
			workflow_type_version: Optional[str] = None,
			tags: Union[str, IO[bytes], None] = None,
			workflow_attachment=None,
			verbose=False
	):

		runURL = self.api_url_base+'/runs'
		if verbose:
			print("sending to {}".format(runURL))

		attachments = {
			'workflow_url': (None, workflow_url,'text/plain'),
			'workflow_params': (None, workflow_params, 'application/json'),
			'workflow_engine_params': (None, workflow_engine_params, 'application/json'),
			'workflow_type': (None, workflow_type, 'text/plain'),
			'workflow_type_version': (None, workflow_type_version, 'text/plain'),
			'tags': (None, tags, 'text/plain'),
			'workflow_attachment': workflow_attachment,
		}

		response = requests.request('POST', runURL, headers=self.headers, files=attachments)
		if verbose:
			print(response.request.body)
			print(response.text)
			print(response)
		if response.status_code == 200:
			return response.json()['run_id']
		elif response.status_code == 401:
			raise RuntimeError("WES server authentication failed")
		else:
			print("Full response status:\n{}".format(response))
			print("Full response content:\n{}".format(response.content))
			raise RuntimeError("WES run submission failed. Response status:{}".format(response.status_code))
