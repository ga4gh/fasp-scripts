''' Query Search SRA BigQuery tables for 1K Genomes data, access files via SRA DRS ids'''
#  IMPORTS
import sys 

from fasp.runner import FASPRunner

# The implementations we're using
from fasp.loc import DRSClient
from fasp.loc import DRSMetaResolver
from fasp.workflow import GCPLSsamtools
from fasp.search import BigQuerySearchClient

def main(argv):


	faspRunner = FASPRunner(pauseSecs=0)
	settings = faspRunner.settings
	# Step 1 - Discovery
	# query for relevant DRS objects
	searchClient = BigQuerySearchClient()

	query = """
		SELECT s.sample_name, drs_id, s.acc, assay_type, filename, 
		FROM `nih-sra-datastore.sra.metadata` s, unnest(attributes) att
		join `isbcgc-216220.onek_genomes.sra_drs_files` d on d.acc = s.acc
		where filetype = 'bam' and mapped = 'mapped' and sequencing_type ='exome'
		and att.k = 'population_sam' and att.v = 'JPT' 
		LIMIT 3"""

	# BioDataCatalyst
	#drsClient = DRSMetaResolver()
	drsClient = DRSClient('https://locate.ncbi.nlm.nih.gov',access_id='2' ,debug=True, public=True)
	location = 'projects/{}/locations/{}'.format(settings['GCPProject'], settings['GCPPipelineRegion'])
	mysam = GCPLSsamtools(location, settings['GCPOutputBucket'])

	faspRunner.configure(searchClient, drsClient, mysam)
		
	faspRunner.runQuery(query, 'One k query SRA DRS')
	    
if __name__ == "__main__":
    main(sys.argv[1:])
