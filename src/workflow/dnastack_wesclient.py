'''
Client for DNAStack WES Service
'''

import requests
import os
import json
import tempfile
import pandas as pd
import sys

from workflow import WESClient

class DNAStackWESClient(WESClient):

	def __init__(self,  access_token_path, debug=False, wdlPath='../../plenary-resources-2020/workflows/'):
		self.api_url_base = 'https://ddap-wes-service.prod.dnastack.com/ga4gh/wes/v1/runs'
		full_key_path = os.path.expanduser(access_token_path)
		with open(full_key_path) as f:
			self.accessToken = json.load(f)['access_token']
		self.headers = { 'Authorization': 'Bearer {}'.format(self.accessToken)}
		self.debug = debug
		self.wdlPath = wdlPath
		
		
	def getTaskStatus(self, run_id):
		runURL = "{}/{}".format(self.api_url_base, run_id)
		runResp = requests.get(runURL, headers=self.headers)
		if runResp.status_code == 200:
			run = runResp.json()
			return run['state']
		if runResp.status_code == 400:
			return 'task not found'


				
	def runWorkflow(self, fileurl, outfile):
		# use a temporary file to write out the input file
		inputJson = {"md5Sum.inputFile":fileurl}
		with tempfile.TemporaryFile() as fp:
			fp.write(json.dumps(inputJson).encode('utf-8'))
			fp.seek(0)
			payload = {'workflow_url': 'checksum.wdl'} 
			files = {
				'workflow_params': ('inputs.json', fp, 'application/json'),
				'workflow_attachment': ('checksum.wdl', open('./workflow/wes/checksum.wdl', 'rb'), 'text/plain')
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
				
				
		
	def runGWASWorkflowTest(self):

		payload = {'workflow_url': 'gwas.wdl'}
		files = {
			'workflow_params': ('inputs.gwas.json', open(self.wdlPath+'inputs.gwas.json', 'rb'), 'application/json'),
			'workflow_attachment': ('gwas.wdl', open(self.wdlPath+'gwas.wdl', 'rb'), 'text/plain')
		}

		response = requests.request("POST", self.api_url_base, headers=self.headers, data = payload, files = files)
		if response.status_code == 200:
			return response.json()['run_id']
		elif response.status_code == 401:
			print("WES server authentication failed")
			sys.exit(1)
		else:
			print("WES run submission failed. Response status:{}".format(response.status_code))
			sys.exit(1)

		return response.json()['run_id']

	def runGWASWorkflow(self, vcfFileurl, csvfileurl):

		# use a temporary file to write out the input file
		inputJson = {"gwas.metadata_csv": csvfileurl, "gwas.vcf": vcfFileurl   }
		with tempfile.TemporaryFile() as fp:
			fp.write(json.dumps(inputJson).encode('utf-8'))
			fp.seek(0)
			payload = {'workflow_url': 'gwas.wdl'}
			files = {
				'workflow_params': ('inputs.gwas.json', fp, 'application/json'),
				'workflow_attachment': ('gwas.wdl', open(self.wdlPath+'gwas.wdl', 'rb'), 'text/plain')
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
		runURL = "{}/{}".format(self.api_url_base, run_id)
		runResp = requests.get(runURL, headers=self.headers)
		run = runResp.json()
		
		runStart = run['run_log']['start_time']
		workflowURL = run['request']['workflow_url']
		params = run['request']['workflow_params']
		newRow =[run_id,runStart,run['state'], workflowURL]
		cols= ["run_id", "start", "state","type"]
		for p, v in params.items():
			newRow.append(v)
			cols.append(p)
		df_row = pd.DataFrame([newRow], columns= cols)
		runsdf = runsdf.append(df_row)
		print(run_id, runStart)
		print (workflowURL, run['state'])
		return runsdf	
	
	def getRuns(self):
		df_columns = ["run_id", "start", "state","type"]
		runsdf = pd.DataFrame(columns = df_columns)

		nextPageToken = ''
		while nextPageToken != 'Done':
			if nextPageToken != '':
				payload = {'page_token': nextPageToken}
			else:
				payload = {}
			response = requests.get(self.api_url_base, headers=self.headers, params=payload)
			rDict = response.json()
			if 'next_page_token' in rDict.keys():
				nextPageToken = rDict['next_page_token']
			else:
				nextPageToken = 'Done'
			
			runs = rDict['runs']
			for r in runs:
				runsdf = self.addRun(r['run_id'], runsdf)
		return runsdf

		
if __name__ == "__main__":
	myClient = DNAStackWESClient('~/.keys/DNAStackWESkey.json')

	res = myClient.runGWASWorkflowTest()
	#res = myClient.runWorkflow('gs://dnastack-public-bucket/thousand_genomes_meta.csv', '')


	print(res)
