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

	def runWorkflow(self, fileurl):
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

		return response
		
	def runGWASWorkflowTest(self):

		payload = {'workflow_url': 'gwas.wdl'}
		files = {
			'workflow_params': ('inputs.gwas.json', open('./wes/gwas/inputs.gwas.json', 'rb'), 'application/json'),
			'workflow_attachment': ('gwas.wdl', open('./wes/gwas/gwas.wdl', 'rb'), 'text/plain')
		}

		headers = {
  			'Authorization': 'Bearer {}'.format(self.accessToken)
		}

		response = requests.request("POST", self.api_url_base, headers=headers, data = payload, files = files)

		return response

	def runGWASWorkflow(self, vcfFileurl, csvfileurl):

		# use a temporary file to write out the input file
		inputJson = {"gwas.metadata_csv": csvfileurl, "gwas.vcf": vcfFileurl   }
		with tempfile.TemporaryFile() as fp:
			fp.write(json.dumps(inputJson).encode('utf-8'))
			fp.seek(0)
			payload = {'workflow_url': 'gwas.wdl'}
			files = {
				'workflow_params': ('inputs.gwas.json', fp, 'application/json'),
				'workflow_attachment': ('gwas.wdl', open('./wes/gwas/gwas.wdl', 'rb'), 'text/plain')
			}

		
			headers = {
  				'Authorization': 'Bearer {}'.format(self.accessToken)
			}

			response = requests.request("POST", self.api_url_base, headers=headers, data = payload, files = files)

		return response
		
if __name__ == "__main__":
	myClient = DNAStackWESClient('~/.keys/DNAStackWESkey.json')

	#res = myClient.runWorkflow('https://storage.googleapis.com/gdc-tcga-phs000178-controlled/f360253c-d7d7-47cb-947a-b26e0b41b800/C499.TCGA-E8-A436-01A-12D-A23U-08.4_gdc_realn.bam?GoogleAccessId=forei-2417@dcf-prod.iam.gserviceaccount.com&Expires=1597432863&Signature=K66pAScp2DYFnaeCdthW8lRkMRODexHHVhe3h5aSBB47X9w2NhVSeDTFF76MQ4x3XWxDTYb3PUZUIKVUGTl753mwQEMI2r0dHP0JdWdG0CcZktZa8l6AuQgl%2BH1oAFraiAUwjNTt7XL1vOriNd2rrNelCYIUusfhW6avklyR3jMssOeeR3LfNLRZzb%2FxRP4eo%2BjXQqpWf63bKJ23PGyOAfNDA8pGuHLT7q98nIHApB5kJjlTnzZ50P0LzCQIkYx%2F4Se1bhRQ3%2FvCOgZX6MYbxDDIjkbKQ7JRDAnY%2FKTE4y9PAU79vJNcw%2FJPnvIi%2FxZ%2By5i2eXwwHo%2BSzScUnJnYlA==')
	res = myClient.runGWASWorkflowTest()
	#res = myClient.runGWASWorkflow('gs://fc-56ac46ea-efc4-4683-b6d5-6d95bed41c5e/CCDG_13607/Project_CCDG_13607_B01_GRM_WGS.JGVariants.2019-04-04/CCDG_13607_B01_GRM_WGS_2019-02-19_chr21.recalibrated_variants.vcf.gz',
	#	'gs://dnastack-public-bucket/thousand_genomes_meta.csv')
	print(res.text.encode('utf8'))
	print (res.json()['run_id'])
