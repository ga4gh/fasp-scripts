import json
import os

from fasp.workflow import WESClient


class ElixirWESClient(WESClient):
	"""
	Client for ELIXIR WES Service
	"""

	def __init__(self, api_base_url, client_credentials_path=None, debug=False):
		self.api_base = api_base_url
		if client_credentials_path == None:
			client_credentials_path = '~/.keys/elixir_wes_credentials.json'
		super(ElixirWESClient, self).__init__(api_base_url)
		full_credentials_path = os.path.expanduser(client_credentials_path)
		with open(full_credentials_path) as f:
			self.credentials = json.load(f)
		if 'access_token' not in self.credentials:
			raise RuntimeError('Must define "access_token" in credentials file')
		self.headers['Authorization'] = 'Bearer {}'.format(self.credentials['access_token'])
		self.debug = debug
		self.modulePath = os.path.dirname(os.path.abspath(__file__))
		self.wdlPath = self.modulePath + '/wes/gwas'

	def run_workflow(self, path, outFile):
		# use a temporary file to write out the input file
		workflow_url = 'https://github.com/uniqueg/cwl-example-workflows/blob/master/hashsplitter-workflow.cwl'
		params = {
			'input': {
				'class': 'File',
				'path': path
			}
		}

		return self.run_generic_workflow(
			workflow_url=workflow_url,
			workflow_params=json.dumps(params),
			workflow_type='CWL',
			workflow_type_version='v1.0',
			verbose = self.debug
		)


if __name__ == "__main__":
	myClient = ElixirWESClient(debug=True)

	res = myClient.run_workflow('http://62.217.82.57/test.txt')
	#res = myClient.get_runs()

	print(res)
