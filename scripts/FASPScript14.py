''' Query Search SRA tables for 1K Genomes data, access files via SRA DRS ids'''
#  IMPORTS
import sys

from fasp.runner import FASPRunner

# The implementations we're using
from fasp.loc import DRSClient
from fasp.workflow import GCPLSsamtools
from fasp.search import DataConnectClient

def main(argv):


	faspRunner = FASPRunner(pauseSecs=0)
	settings = faspRunner.settings
	# Step 1 - Discovery
	# query for relevant DRS objects
	searchClient = DataConnectClient('https://publisher-data.publisher.dnastack.com/data-connect/', debug=True)

	query = "SELECT s.su_submitter_id, drs_id FROM collections.public_datasets.onek_genomes_ssd_drs s join collections.public_datasets.onek_genomes_sra_drs_files f on f.sample_name = s.su_submitter_id where filetype = 'bam' and mapped = 'mapped' and sequencing_type ='exome' and  population = 'JPT' LIMIT 3"

	drsClient = DRSClient('https://locate.ncbi.nlm.nih.gov',access_id='2' ,debug=True, public=True)
	location = 'projects/{}/locations/{}'.format(settings['GCPProject'], settings['GCPPipelineRegion'])
	mysam = GCPLSsamtools(location, settings['GCPOutputBucket'])

	faspRunner.configure(searchClient, drsClient, mysam)

	faspRunner.runQuery(query, 'One k query SRA DRS')

if __name__ == "__main__":
    main(sys.argv[1:])
