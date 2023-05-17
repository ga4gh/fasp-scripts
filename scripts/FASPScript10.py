#  IMPORTS
import sys

from fasp.runner import FASPRunner

# The implementations we're using
from fasp.loc import DRSMetaResolver
from fasp.search import DataConnectClient
from fasp.workflow import DNAStackWESClient


def main(argv):

	faspRunner = FASPRunner(pauseSecs=0)


	pp_dbgap_join = """
	SELECT
		sp.dbGaP_Subject_ID,
		'sbcgc:' || sb_drs_id
	FROM collections.public_datasets.dbgap_scr_gecco_susceptibility_subject_phenotypes_multi sp
	JOIN collections.public_datasets.dbgap_scr_gecco_susceptibility_sample_multi sm
		ON sm.dbgap_subject_id = sp.dbgap_subject_id
	JOIN collections.public_datasets.dbgap_scr_gecco_susceptibility_sb_drs_index di
		ON di.sample_id = sm.sample_id
	JOIN collections.public_datasets.sample_phenopackets_gecco_phenopackets pp
		ON pp.id = sm.biosample_accession
	WHERE json_extract_scalar(pp.phenopacket, '$.subject.sex') = 'MALE'
		AND file_type = 'cram'
	LIMIT 3
	"""

	# Step 1 - Discovery
	# query for relevant DRS objects
	searchClient = DataConnectClient('https://publisher-data.publisher.dnastack.com/data-connect/', debug=True)

	# Step 2 - DRS - a metaresolver will deal with which drs server is required
	drsClient = DRSMetaResolver()

	# Step 3 - set up a class that run a compute for us
	wesClient = DNAStackWESClient('~/.keys/dnastack_wes_credentials.json')

	faspRunner.configure(searchClient, drsClient, wesClient)

	faspRunner.runQuery(pp_dbgap_join, 'Phenopacket Gecco')

if __name__ == "__main__":
	main(sys.argv[1:])
