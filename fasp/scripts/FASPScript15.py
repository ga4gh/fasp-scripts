''' Compute on ANVIL GTEX files'''
#  IMPORTS
import sys
import json 

from fasp.runner import FASPRunner

# The implementations we're using
from fasp.loc import Gen3DRSClient
from fasp.workflow import GCPLSsamtools


class localSearchClient:
	
	def __init__(self):
		# edit the following for yuor local copy of the manifest file
		with open('/users/forei/fasp/gtex/gtex-cram-manifest.json') as f:
			self.data = json.load(f)
			
	def runQuery(self, query):
		# return the first three records
		# edit this once your ready to run this on all the files
		results = []
		for f in self.data[:1]:
			results.append([f['file_name'],f['object_id']])
		return  results

def main(argv):


	faspRunner = FASPRunner(pauseSecs=0)
	settings = faspRunner.settings
	# Step 1 - Discovery
	# query for relevant DRS objects
	searchClient = localSearchClient()

	#drsClient = DRSMetaResolver()
	drsClient = Gen3DRSClient('https://gen3.theanvil.io','/user/credentials/api/access_token', '~/.keys/anvil_credentials.json', 'gs')
	location = 'projects/{}/locations/{}'.format(settings['GCPProject'], settings['GCPPipelineRegion'])
	mysam = GCPLSsamtools(location, settings['GCPOutputBucket'], debug=True)

	faspRunner.configure(searchClient, drsClient, mysam)
		
	faspRunner.runQuery('', 'Anvil GTEX Test')
	
if __name__ == "__main__":
	main(sys.argv[1:])


