import requests
import os
import json
import tempfile

from WESClient import WESClient 

class DNAStackWESClient(WESClient):

    
	def __init__(self,  access_token_path):
		self.api_url_base = 'https://ddap-wes-service.prod.dnastack.com/ga4gh/wes/v1/runs'
		full_key_path = os.path.expanduser(access_token_path)
		with open(full_key_path) as f:
			self.accessToken = json.load(f)['access_token']

	def runWorkflow(self, fileurl, outfile):
		# use a temporary file to write out the input file
		inputJson = {"md5Sum.inputFile":fileurl}
		with tempfile.TemporaryFile() as fp:
			fp.write(json.dumps(inputJson).encode('utf-8'))
			fp.seek(0)
			payload = {'workflow_url': 'checksum.wdl'}
			files = {
				'workflow_params': ('inputs.json', fp, 'application/json'),
				'workflow_attachment': ('checksum.wdl', open('./wes/checksum.wdl', 'rb'), 'text/plain')
			}

		
			headers = {
  				'Authorization': 'Bearer {}'.format(self.accessToken)
			}

			response = requests.request("POST", self.api_url_base, headers=headers, data = payload, files = files)

		return response.json()['run_id']
		
	def runGWASWorkflowTest(self):

		payload = {'workflow_url': 'gwas.wdl'}
		files = {
			'workflow_params': ('inputs.gwas.json', open('../plenary-resources-2020/workflows/inputs.gwas.json', 'rb'), 'application/json'),
			'workflow_attachment': ('gwas.wdl', open('../plenary-resources-2020/workflows/gwas.wdl', 'rb'), 'text/plain')
		}

		headers = {
  			'Authorization': 'Bearer {}'.format(self.accessToken)
		}

		response = requests.request("POST", self.api_url_base, headers=headers, data = payload, files = files)

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
				'workflow_attachment': ('gwas.wdl', open('../plenary-resources-2020/workflows/gwas.wdl', 'rb'), 'text/plain')
			}

		
			headers = {
  				'Authorization': 'Bearer {}'.format(self.accessToken)
			}

			response = requests.request("POST", self.api_url_base, headers=headers, data = payload, files = files)

		return response
		
if __name__ == "__main__":
	myClient = DNAStackWESClient('~/.keys/DNAStackWESkey.json')

	#res = myClient.runGWASWorkflowTest()
	res = myClient.runWorkflow('gs://dnastack-public-bucket/thousand_genomes_meta.csv', '')
	#res = myClient.runGWASWorkflow('gs://fc-56ac46ea-efc4-4683-b6d5-6d95bed41c5e/CCDG_13607/Project_CCDG_13607_B01_GRM_WGS.JGVariants.2019-04-04/CCDG_13607_B01_GRM_WGS_2019-02-19_chr21.recalibrated_variants.vcf.gz',
	#	'gs://dnastack-public-bucket/thousand_genomes_meta.csv')
	print(res)
