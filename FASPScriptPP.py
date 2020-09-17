#  IMPORTS
import sys, getopt, os
import json
import collections 


from BigQuerySearchClient import BigQuerySearchClient
from DiscoverySearchClient import DiscoverySearchClient



def main(argv):


	searchClient = DiscoverySearchClient('https://ga4gh-search-adapter-presto-public.prod.dnastack.com/')
	#query = "select id, phenopacket from sample_phenopackets.ga4gh_tables.gecco_phenopackets limit 10"
	query = "select id from sample_phenopackets.ga4gh_tables.gecco_phenopackets where json_extract_scalar(phenopacket, '$.subject.sex') = 'MALE'"
	
	bqSearchClient = BigQuerySearchClient()
	#query = "select id, phenopacket from sample_phenopackets.ga4gh_tables.gecco_phenopackets limit 10"

	crdcquery = """
		SELECT BioSample_Accession id
		FROM `isbcgc-216220.GECCO_CRC_Susceptibility.Subject_Phenotypes` sp
		join `isbcgc-216220.GECCO_CRC_Susceptibility.Sample_MULTI` sm on sm.dbgap_subject_id = sp.dbgap_subject_id
		and sex = 'Male'
		"""

	dbList = []
	results = bqSearchClient.runQuery(crdcquery)
	print(len(results))	
	for r in results:
		dbList.append(r['id'])
	ppList = []
	query_job = searchClient.runQuery(query)  # Send the query
	print(len(query_job))
	for r in query_job:
		ppList.append(r[0])
		
	# compare the lists
	dbList.sort() 
	ppList.sort() 
	if dbList == ppList: 
		print ("The lists dbList and ppList are the same") 
	else: 
		print ("The lists dbList and ppList are not the same") 
    
# 	for row in query_job:
# 		sex = row[1]
# 		print("id={} sex={}".format(row[0],sex))

    
if __name__ == "__main__":
    main(sys.argv[1:])
    


	
	

	
	









