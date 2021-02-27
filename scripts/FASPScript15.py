''' Compute on ANVIL GTEX files'''
#  IMPORTS
import sys
import json 

from fasp.runner import FASPRunner

# The implementations we're using
from fasp.loc import Gen3DRSClient
from fasp.workflow import GCPLSsamtools
from fasp.loc import anvilDRSClient


class localSearchClient:
	
	def __init__(self):
		# edit the following for your local copy of the manifest file
		with open('../fasp/data/gtex/gtex-cram-manifest.json') as f:
			self.data = json.load(f)
			
	def runQuery(self, query):
		# return the first three records
		# edit this once your ready to run this on all the files
		results = []
		for f in self.data[query:query+3]:
			results.append([f['file_name'],f['object_id']])
		return  results

def main(argv):

	# edit the following line for where you put your credentials file from anvil
	credentials_file = '~/.keys/anvil_credentials.json'

	faspRunner = FASPRunner(pauseSecs=0)
	settings = faspRunner.settings
	# Step 1 - Discovery
	# query for relevant DRS objects
	searchClient = localSearchClient()

	#drsClient = DRSMetaResolver()

	drsClient = anvilDRSClient(credentials_file, settings['GCPProject'], 'gs')
	location = 'projects/{}/locations/{}'.format(settings['GCPProject'], settings['GCPPipelineRegion'])
	workflowClient = GCPLSsamtools(location, settings['GCPOutputBucket'])

	faspRunner.configure(searchClient, drsClient, workflowClient)
		
	faspRunner.runQuery(12, 'Anvil GTEX Test')
	
if __name__ == "__main__":
	main(sys.argv[1:])


