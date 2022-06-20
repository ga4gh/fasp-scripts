'''
Client for Seven Bridges WES Service
'''

import requests
import os
import json
import tempfile
import pandas as pd
import sys

from fasp.workflow import WESClient
from fasp.loc import DRSMetaResolver

class sbWESClient(WESClient):

	def __init__(self, api_url_base, project, access_token_path, instance=None, debug=False):
		
		# instance is now redundant - use specific subclasses instead. Left in for legacy compatibility
		
		self.project_id = project
				
		self.api_url_base = api_url_base
		full_key_path = os.path.expanduser(access_token_path)
		with open(full_key_path) as f:
			self.accessToken = json.load(f)['access_token']
		self.headers = { 'X-SBG-Auth-Token': self.accessToken}
		self.debug = debug
		self.modulePath = os.path.dirname(os.path.abspath(__file__))
		self.mr = None

	
	def __getMR(self):
		if self.mr is None:
			self.mr = DRSMetaResolver()
		return self.mr

	def runGWASWorkflow(self, vcfFileurl, csvfileurl):
		''' run the plenary GWAS Workflow '''
		# use a temporary file to write out the input file
		inputJson = {"gwas.metadata_csv": csvfileurl, "gwas.vcf": vcfFileurl   }
		with tempfile.TemporaryFile() as fp:
			fp.write(json.dumps(inputJson).encode('utf-8'))
			fp.seek(0)
			payload = {'workflow_url': 'gwas.wdl'}
			files = {
				'workflow_params': ('inputs.gwas.json', fp, 'application/json'),
				'workflow_attachment': ('gwas.wdl', open(self.wdlPath+'/gwas.wdl', 'rb'), 'text/plain')
			}

		
			response = requests.request("POST", self.api_url_base, headers=self.headers, data = payload, files = files)
			if self.debug:
				print(response)
			if response.status_code == 200:
				return response.json()['run_id']
			elif response.status_code == 401:
				print("WES server authentication failed")
				sys.exit(1)
			else:
				print("WES run submission failed. Response status:{}".format(response.status_code))
				sys.exit(1)

		return response.json()['run_id']
		
		
	def addRun(self, run_id, runsdf):
		runURL = "{}/{}".format(self.api_url_base+'/runs', run_id)
		if self.debug:
			print("sending {}".format(runURL))
		runResp = requests.get(runURL, headers=self.headers)
		run = runResp.json()
		#if self.debug:
		#	print(json.dumps(run, indent=3))
		
		try:
			runStart = run['run_log']['start_time']
			if 'workflow_url' in run['request']:
				workflowURL = run['request']['workflow_url']
			else:
				workflowURL = 'unknown'
			params = run['request']['workflow_params']
			newRow =[run_id,runStart,run['state'], workflowURL]
			if self.debug:
				print(newRow)
			cols= ["run_id", "start", "state","type"]
			for p, v in params.items():
				newRow.append(v)
				cols.append(p)
			df_row = pd.DataFrame([newRow], columns= cols)
			runsdf = runsdf.append(df_row)
		except KeyError as err:
			print(json.dumps(run, indent=3))
			print (err)
		#print(run_id, runStart)
		#print (workflowURL, run['state'])
		return runsdf	
	
	def getRuns(self):
		df_columns = ["run_id", "start", "state","type"]
		runsdf = pd.DataFrame(columns = df_columns)

		nextPageToken = ''
		while nextPageToken != None:
			if nextPageToken != '':
				payload = {'page_token': nextPageToken}
			else:
				payload = {}
			response = requests.get(self.api_url_base+'/runs', headers=self.headers, params=payload)
			if self.debug:
				print(json.dumps(response.json(), indent=3))
			rDict = response.json()
			if 'next_page_token' in rDict.keys():
				nextPageToken = rDict['next_page_token']
				if nextPageToken == "":
					nextPageToken = None
			else:
				nextPageToken = None
			
			for r in rDict['runs']:
				print(r['run_id'],r['state'])
			#runs = rDict['runs']
			#for r in runs:
			#	runsdf = self.addRun(r['run_id'], runsdf)
		return runsdf

class sbcgcWESClient(sbWESClient):
	'''client for Seven Bridges Cancer Genomics Cloud WES server'''

	def __init__(self, project, api_key_path=None, debug=False):
		if api_key_path == None: api_key_path='~/.keys/sbcgc_key.json'
		super().__init__('https://cgc-ga4gh-api.sbgenomics.com/ga4gh/wes/v1', project, api_key_path, debug=debug)

class cavaticaWESClient(sbWESClient):
	'''client for Cavatica WES Server'''    

	def __init__(self, project, api_key_path=None, debug=False):
		if api_key_path == None: api_key_path='~/.keys/sbcav_key.json'
		super().__init__('https://cavatica-ga4gh-api.sbgenomics.com/ga4gh/wes/v1', project, api_key_path, debug=debug)

		
if __name__ == "__main__":
	myClient = sbWESClient('https://cgc-ga4gh-api.sbgenomics.com/ga4gh/wes/v1','user/project','~/.keys/sbcgc_key.json')
	res = myClient.getRuns()
	print(res)
