import json
import os
import tempfile
import time

import pandas as pd
import requests

from fasp.workflow import WESClient


class DNAStackWESClient(WESClient):
	"""
	Client for DNAStack WES Service
	"""

	def __init__(self, client_credentials_path, debug=False):
		super(DNAStackWESClient, self).__init__('https://workspaces-wes.beta.dnastack.com/ga4gh/wes/v1')
		self.tokenUrl = 'https://wallet.prod.dnastack.com/oauth/token'
		full_credentials_path = os.path.expanduser(client_credentials_path)
		with open(full_credentials_path) as f:
			self.credentials = json.load(f)
			self.__updateAccessToken()
		self.headers['Authorization'] = 'Bearer {}'.format(self.accessToken)
		self.debug = debug
		self.modulePath = os.path.dirname(os.path.abspath(__file__))
		self.wdlPath = self.modulePath + '/wes/gwas'

	def __updateAccessToken(self):
		if 'id' not in self.credentials or 'secret' not in self.credentials:
			raise RuntimeError('Credentials file must have "id" and "secret" values')
		payload = [
			('grant_type', 'client_credentials'),
			('client_id', self.credentials['id']),
			('client_secret', self.credentials['secret']),
			# technically only need one of these
			# future-proofing against support for DNAstack policy engine
			#('resource', 'https://workspaces-wes.prod.dnastack.com')
			#('resource', self.api_url_base + '/')
			('resource', self.api_url_base + '/runs'),
			('resource', self.api_url_base + '/runs/')
		]
		response = requests.post(self.tokenUrl, data=payload)
		if response.status_code == 200:
			body = response.json()
			self.accessToken = body['access_token']
		else:
			print("error getting token. status=%d, body=%s" % (response.status_code, response.content))
			raise RuntimeError('unable to get DNAstack access token')

	def runWorkflow(self, fileurl, outfile):
		# use a temporary file to write out the input file
		inputs = {"md5Sum.inputFile": fileurl}

		return self.runGenericWorkflow(
			workflow_url='checksum.wdl',
			workflow_params=json.dumps(inputs),
			workflow_attachment=('checksum.wdl', open(self.modulePath+'/wes/checksum.wdl', 'rb'), 'text/plain'),
			verbose = self.debug
		)
		
	def runGWASWorkflowTest(self):
		''' run the GWAS workflow by submitting local files '''

		return self.runGenericWorkflow(
			workflow_url='gwas.wdl',
			workflow_params=open(self.wdlPath+'/inputs.gwas.json', 'rb'),
			workflow_attachment=('gwas.wdl', open(self.wdlPath+'/gwas.wdl', 'rb'), 'text/plain')
		)


	def runGWASWorkflow(self, vcfFileurl, csvfileurl):
		''' run the GWAS workflow by using files accessed by DRS'''
		# use a temporary file to write out the input file
		inputJson = {"gwas.metadata_csv": csvfileurl, "gwas.vcf": vcfFileurl   }
		with tempfile.TemporaryFile() as fp:
			fp.write(json.dumps(inputJson).encode('utf-8'))
			fp.seek(0)
			payload = {
				'workflow_url': 'gwas.wdl',
				'workflow_params': ('inputs.gwas.json', fp, 'application/json'),
				'workflow_attachment': ('gwas.wdl', open(self.wdlPath+'/gwas.wdl', 'rb'), 'text/plain')
			}

			return self.runGenericWorkflow(
				workflow_url='gwas.wdl',
				workflow_params=fp,
				workflow_attachment=('gwas.wdl', open(self.wdlPath+'/gwas.wdl', 'rb'), 'text/plain')
			)

		
	def addRun(self, run_id, runsdf):
		runURL = "{}/runs/{}".format(self.api_url_base, run_id)
		runResp = requests.get(runURL, headers=self.headers)
		if self.debug: print(json.dumps(runResp.json(), indent=3))
		run = runResp.json()
		
		if 'run_log' in run:
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
		url = self.api_url_base + '/runs'
		if self.debug: print(url)
		while nextPageToken != 'Done':
			if nextPageToken != '':
				payload = {'page_token': nextPageToken}
			else:
				payload = {}
			response = requests.get(url, headers=self.headers, params=payload)
			if self.debug: print(json.dumps(response.json(), indent=3))
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
	myClient = DNAStackWESClient('~/.keys/dnastack_wes_credentials.json')
	run_id = myClient.runWorkflow('gs://dnastack-public-bucket/thousand_genomes_meta.csv', '')

	status = myClient.getTaskStatus(run_id)
	# TODO make sure this is exhaustive
	while status not in {'RUNNING', 'COMPLETED', 'FAILED'}:
		time.sleep(5)
		status = myClient.getTaskStatus(run_id)
		print('Task Status: ' + status)
	print('Workflow started successfully')
	print('Workflow run id: ' + run_id)
