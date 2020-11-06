#  IMPORTS
import sys 

from fasp.search import DiscoverySearchClient


def main(argv):



	pp_dbgap_join = "SELECT sp.dbGaP_Subject_ID,  'sbcgc:'||sb_drs_id FROM dbgap_demo.scr_gecco_susceptibility.subject_phenotypes_multi sp join dbgap_demo.scr_gecco_susceptibility.sample_multi sm on sm.dbgap_subject_id = sp.dbgap_subject_id join dbgap_demo.scr_gecco_susceptibility.sb_drs_index di on di.sample_id = sm.sample_id join sample_phenopackets.ga4gh_tables.gecco_phenopackets pp on pp.id = sm.biosample_accession where  json_extract_scalar(pp.phenopacket, '$.subject.sex') = 'MALE' and file_type = 'cram' limit 3"
		
	# Step 1 - Discovery
	# query for relevant DRS objects
	searchClient = DiscoverySearchClient('https://ga4gh-search-adapter-presto-public.prod.dnastack.com/', debug=True)

	results = searchClient.runQuery(pp_dbgap_join)
	
		# repeat steps 2 and 3 for each row of the query
	for row in results:

		print("subject={}, drsID={}".format(row[0], row[1]))

if __name__ == "__main__":
	main(sys.argv[1:])
