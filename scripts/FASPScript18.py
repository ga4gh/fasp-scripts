''' Compute on ANVIL GTEX files from AWS on SevenBridges WES Platform'''
#  IMPORTS
import sys

from fasp.runner import FASPRunner

# The implementations we're using
from fasp.workflow import sbWESClient
from fasp.loc import anvilDRSClient
from fasp.search import Gen3ManifestClient




def main(argv):

	faspRunner = FASPRunner()
	settings = faspRunner.settings

	searchClient = Gen3ManifestClient('./fasp/data/gtex/gtex-cram-manifest.json')

	drsClient = anvilDRSClient('~/.keys/anvil_credentials.json', access_id='s3')

	wesClient = sbWESClient(settings['SevenBridgesInstance'], settings['SevenBridgesProject'],
                        '~/.keys/sbcgc_key.json')

	faspRunner.configure(searchClient, drsClient, wesClient)
		
	faspRunner.runQuery(3, 'Anvil GTEX Test')
	
if __name__ == "__main__":
	main(sys.argv[1:])