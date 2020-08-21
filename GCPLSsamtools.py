"""
BEFORE RUNNING:
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
"""
from pprint import pprint
import tempfile
import subprocess

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

import json

credentials = GoogleCredentials.get_application_default()

service = discovery.build('lifesciences', 'v2beta', credentials=credentials)
#service = discovery.build('lifesciences', 'v2beta')

# The project and location that this request should be executed against.
parent = 'projects/isbcgc-216220/locations/us-central1'  # TODO: Update placeholder value.


class GCPLSsamtools:

	def __init__(self, outdir ):
		self.outdir = outdir


	def runStats(self, bamURL, outfile):
		samtools = {
		  "imageUri": "gcr.io/genomics-tools/samtools",
		  "commands": [
			"-c, samtools stats ${BAM} > ${STATS}"
		  ],
		  "entrypoint": "bash",
		  "mounts": [
		  {
			"disk": "gcloud-shared",
			"path": "/gcloud-shared"
		  }
		  ]
		}
		
		copyCommand = '/bin/sh, -c, gsutil -m -q cp ${STATS} '+ self.outdir + outfile
		copy = {
		  "imageUri": "google/cloud-sdk:slim",
		  "commands": [
			copyCommand
		  ],
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
		print (run_pipeline_request_body)
		request = service.projects().locations().pipelines().run(parent=parent, body=run_pipeline_request_body)
		response = request.execute()

		return(response)

	def statsCommandLine(self, bamURL, outfile):
		cline = "gcloud beta lifesciences pipelines run --command-line 'samtools stats ${BAM} > ${STATS}' "
		cline += "--docker-image \"gcr.io/genomics-tools/samtools\" --regions us-east1 " 
		cline += "--inputs BAM=\"" + bamURL + "\" "
		cline += "--outputs  STATS=" + self.outdir + outfile
		print (cline)
		return cline

	def runWorkflow(self, bamURL, outfile):
		#runStats above should have allowed us to submit a pipeline - but the pipelines fail
		# This is the workaround - just create a shell script		
		cline = self.statsCommandLine(bamURL, outfile)
		with tempfile.NamedTemporaryFile(mode='w') as shellScript:
			shellScript.write(cline)
			shellScript.write("\n")
			shellScript.flush()
			#res = subprocess.run(['sh', shellScript.name])
		return ''

    
		
