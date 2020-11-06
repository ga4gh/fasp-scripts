#  IMPORTS
#from google.cloud import bigquery
import sys


from fasp.search import BigQuerySearchClient, DiscoverySearchClient



def main(argv):

	
	# Step 1 - Discovery
	# query for relevant DRS objects
	discoveryClients = {
		"sb": DiscoverySearchClient('https://ga4gh-search-adapter-presto-public.prod.dnastack.com/'),
		"bdc": BigQuerySearchClient()
	}

	crdcquery = "SELECT sp.dbGaP_Subject_ID,  'sb:'||sb_drs_id FROM dbgap_demo.scr_gecco_susceptibility.subject_phenotypes_multi sp join dbgap_demo.scr_gecco_susceptibility.sample_multi sm on sm.dbgap_subject_id = sp.dbgap_subject_id join dbgap_demo.scr_gecco_susceptibility.sb_drs_index di on di.sample_id = sm.sample_id where AGE between 45 and 55 and sex = 'Female' and file_type = 'cram' limit 3"
		


	bdcquery = """
		SELECT sp.dbGaP_Subject_ID,  'bdc:'||read_drs_id
		FROM `isbcgc-216220.COPDGene.Subject_MULTI` sm
		join `isbcgc-216220.COPDGene.Subject_Phenotypes_HMB` sp on sp.dbgap_subject_id = sm.dbgap_subject_id
		join `isbcgc-216220.COPDGene.COPD_DRS` drs on drs.su_submitter_id = sm.subject_id
 		where gender = '2'
 		and Age_Enroll between 45 and 55
 		LIMIT 3"""
		

	results = discoveryClients['sb'].runQuery(crdcquery)  # Send the query
	results += discoveryClients['bdc'].runQuery(bdcquery) 
	


	
	# repeat steps 2 and 3 for each row of the query
	for row in results:

		print("subject={}, drsID={}".format(row[0], row[1]))

if __name__ == "__main__":
	main(sys.argv[1:])
