''' Compute on ANVIL GTEX files'''
#  IMPORTS
import sys
import json 

from fasp.loc import anvilDRSClient


def main(argv):

	drs_id = argv[0]
	gcp_project = argv[1]
	# edit the following line for where you put your credentials file from anvil
	credentials_file = '~/.keys/anvil_credentials.json'

	drsClient = anvilDRSClient(credentials_file, gcp_project, 'gs')
	url = drsClient.getAccessURL(drs_id)
	print(url)

	
if __name__ == "__main__":
	main(sys.argv[1:])


