#  IMPORTS
import sys

from DiscoverySearchClient import DiscoverySearchClient



def main(argv):

	searchClient = DiscoverySearchClient('https://ga4gh-search-adapter-presto-public.prod.dnastack.com/', debug=False)


	dbgap_query = """select sm.biosample_accession, sp.sex dbgap_sex FROM dbgap_demo.scr_gecco_susceptibility.subject_phenotypes_multi sp join dbgap_demo.scr_gecco_susceptibility.sample_multi sm on sm.dbgap_subject_id = sp.dbgap_subject_id"""

	dbgap_query2 = """select sp.sex dbgap_sex FROM dbgap_demo.scr_gecco_susceptibility.subject_phenotypes_multi sp"""

	dbgap_query3 = """select sm.biosample_accession FROM dbgap_demo.scr_gecco_susceptibility.sample_multi sm"""

#	query_job = searchClient.runQuery(dbgap_query2)  # Send the query
#	print(len(query_job))
# 	for r in query_job:
# 		print (r)
		
	pp_dbgap_join = "select sm.biosample_accession, sp.sex dbgap_sex, json_extract_scalar(pp.phenopacket, '$.subject.sex') FROM dbgap_demo.scr_gecco_susceptibility.subject_phenotypes_multi sp join dbgap_demo.scr_gecco_susceptibility.sample_multi sm on sm.dbgap_subject_id = sp.dbgap_subject_id join sample_phenopackets.ga4gh_tables.gecco_phenopackets pp on pp.id = sm.biosample_accession"

	query_job = searchClient.runQuery(pp_dbgap_join)  # Send the query
	print(len(query_job))
	for r in query_job:
		print (r)
		
    
if __name__ == "__main__":
    main(sys.argv[1:])
	



	
	

	
	









