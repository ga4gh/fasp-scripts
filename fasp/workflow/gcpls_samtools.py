'''
Wrapper to prepare a job to run samtools as a GCP Life Sciences pipeline.
'''
'''BEFORE RUNNING:
---------------
1. If not already done, enable the Cloud Life Sciences API
   and check the quota for your project at
   https://console.developers.google.com/apis/api/lifesciences
2. This sample uses Application Default Credentials for authentication.
   If not already done, install the gcloud CLI from
   https://cloud.google.com/sdk and run
   `gcloud beta auth application-default login`.
   For more information, see
   https://developers.google.com/identity/protocols/application-default-credentials
3. Install the Python client library for Google APIs by running
   `pip install --upgrade google-api-python-client`
'''

import tempfile
import subprocess
import sys


from googleapiclient import discovery
from google.cloud import storage
from oauth2client.client import GoogleCredentials

import json

class GCPLSsamtools:

	def __init__(self, projectLocation, outdir, debug=False ):
		self.projectLocation = projectLocation
		self.outdir = outdir
		credentials = GoogleCredentials.get_application_default()
		self.service = discovery.build('lifesciences', 'v2beta', credentials=credentials)
		self.debug = debug

	def getTaskStatus(self, run_id):
		# The name of the operation resource.
		name = self.projectLocation + '/operations/' + str(run_id)

		request = self.service.projects().locations().operations().get(name=name)
		response = request.execute()
		if 'done' not in response.keys():
			return 'running'
		if response['done'] == True:
			if 'response' in response.keys():
				return 'Completed'
			else:
				return 'Failed'
		else:
			return 'running'

	def getTaskDetails(self, run_id):
		# The name of the operation resource.
		name = self.projectLocation + '/operations/' + str(run_id)

		request = self.service.projects().locations().operations().get(name=name)
		response = request.execute()

		if self.debug: print(json.dumps(response, indent = 2, ensure_ascii=True))
		return response

	def runStats(self, bamURL, outfile):
		samtools = {
		  "imageUri": "us.gcr.io/isbcgc-216220/samtools",
		  "commands": [
			"-c", "samtools stats ${BAM} > ${STATS}"
		  ],
		  "entrypoint": "bash",
		  "mounts": [
		  {
			"disk": "gcloud-shared",
			"path": "/gcloud-shared"
		  }
		  ]
		}
		
		copyCommands = ['/bin/sh', '-c', 'gsutil -m -q cp ${STATS} '+ self.outdir + outfile]
		copy = {
		  "imageUri": "google/cloud-sdk:slim",
		  "commands": copyCommands ,
		  "mounts": [
		  {
			"disk": "gcloud-shared",
			"path": "/gcloud-shared"
		  }
		  ]
		}

		resources = {
		  "regions": [
			"us-east1"
		  ],
		  "virtualMachine": {
			"machineType": "n1-standard-1",
			"disks": [
			 {
			   "name": "gcloud-shared",
			 }
			 ],
			"serviceAccount": {
			  "scopes": ["https://www.googleapis.com/auth/cloud-platform"]
			 }
		   }
		}

		run_pipeline_request_body = {
		  "pipeline": {
			"actions": [
			  samtools,
			  copy
			 ],
			"resources": resources,
			"environment": {
			  "BAM": bamURL,
			  "STATS": "/gcloud-shared/output0"
			}
		  }
		}
		if self.debug: print ('Pipeline request\n{}'.format(run_pipeline_request_body))
		request = self.service.projects().locations().pipelines().run(parent=self.projectLocation, body=run_pipeline_request_body)
		response = request.execute()
		run_id = response['name'].split('/')[-1]
		return(run_id)

	def runWorkflow(self, bamURL, outfile):
		run_id = self.runStats(bamURL, outfile)		
		return run_id

	def getSAMToolsResults(self, run_id, statsRequired):
		details = self.getTaskDetails(run_id)
		copyCommand = details['metadata']['pipeline']['actions'][1]['commands'][2]
		statsURI = copyCommand.split(' ')[-1]
		parts = statsURI.split('/')
		bucket_name  = parts[3]
		fileName = parts[4]
		print(bucket_name, fileName)
		storage_client = storage.Client()
		bucket = storage_client.bucket(bucket_name)

		# Construct a client side representation of a blob.
		# Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
		# any content from Google Cloud Storage. As we don't need additional data,
		# using `Bucket.blob` is preferred here.
		blob = bucket.blob(fileName)
		
		downloaded_blob = blob.download_as_string()
		print(downloaded_blob)

		#=======================================================================
		# gcs_file = gcs.open(statsURI)
  # 		contents = gcs_file.read()
  #   	gcs_file.close()
  #    	self.response.write(contents)
		# retDict = {}
		# with tempfile.NamedTemporaryFile(mode='r+') as file:
		# 	response = requests.get(url)
		# 	file.write(response.text)
		# 	file.seek(0)
		# 	for x in file:
		# 		if x.startswith('SN'):   
		# 			parts = x.split('\t')
		# 			statName = parts[1].split(':')[0]
		# 			if statName in statsRequired:
		# 				retDict[statName] = parts[2].rstrip()
		#=======================================================================
		return statsURI

	''' build a gloud command line to run samtools '''
	def statsCommandLine(self, bamURL, outfile):
		cline = "gcloud beta lifesciences pipelines run --command-line 'samtools stats ${BAM} > ${STATS}' "
		# note original used gcr.io/genomics-tools/samtools which is samtools 1.6. It may suit your purposes.
        # The following is a deployment of a custom docker image containing samtools 1.8 which is also deployed on Seven Bridges
		cline += "--docker-image \"us.gcr.io/isbcgc-216220/samtools\" --regions us-east1 " 
		cline += "--inputs BAM=\"" + bamURL + "\" "
		#cline += "--billing-project=\"isbcgc-216220\"  "
		cline += "--outputs  STATS=" + self.outdir + outfile
		return cline

	''' Run a workflow by submitting a gloud command as a shell script '''
	def runWorkflowviaGcloud(self, bamURL, outfile):
		cline = self.statsCommandLine(bamURL, outfile)
		if self.debug:
			print (cline)
		with tempfile.NamedTemporaryFile(mode='w') as shellScript:
			shellScript.write(cline)
			shellScript.write("\n")
			shellScript.flush()
			res = subprocess.run(['sh', shellScript.name], capture_output=True, text=True)
			parts = re.split('/|].', res.stderr)
			run_id = parts[-2]

		return run_id

if __name__ == "__main__":
	client = GCPLSsamtools('projects/isbcgc-216220/locations/us-central1','')
	client.getTaskDetails(sys.argv[1])
