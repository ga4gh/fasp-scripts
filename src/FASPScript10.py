#  IMPORTS
import sys 

from runner import FASPRunner

# The implementations we're using
from loc import DRSMetaResolver
from search import DiscoverySearchClient
from workflow import DNAStackWESClient


def main(argv):

	faspRunner = FASPRunner("./pipelineLog.txt", pauseSecs=0)


	pp_dbgap_join = "SELECT sp.dbGaP_Subject_ID,  'sbcgc:'||sb_drs_id FROM dbgap_demo.scr_gecco_susceptibility.subject_phenotypes_multi sp join dbgap_demo.scr_gecco_susceptibility.sample_multi sm on sm.dbgap_subject_id = sp.dbgap_subject_id join dbgap_demo.scr_gecco_susceptibility.sb_drs_index di on di.sample_id = sm.sample_id join sample_phenopackets.ga4gh_tables.gecco_phenopackets pp on pp.id = sm.biosample_accession where  json_extract_scalar(pp.phenopacket, '$.subject.sex') = 'MALE' and file_type = 'cram' limit 3"
		
	# Step 1 - Discovery
	# query for relevant DRS objects
	searchClient = DiscoverySearchClient('https://ga4gh-search-adapter-presto-public.prod.dnastack.com/', debug=True)

	# Step 2 - DRS - a metaresolver will deal with which drs server is required
	drsClient = DRSMetaResolver()

	# Step 3 - set up a class that run a compute for us
	wesClient = DNAStackWESClient('~/.keys/DNAStackWESkey.json')
	
	faspRunner.configure(searchClient, drsClient, wesClient)
		
	faspRunner.runQuery(pp_dbgap_join, 'Phenopacket Gecco')

if __name__ == "__main__":
	main(sys.argv[1:])
