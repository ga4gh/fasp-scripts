''' Compares gecco data from Biosamples Phenopackets with dbGap Gecco Subject_phenotype'''
#  IMPORTS
import sys, getopt, os
import json
import collections


from fasp.search import BigQuerySearchClient
from fasp.search import DataConnectClient



def main(argv):


	searchClient = DataConnectClient('https://publisher-data.publisher.dnastack.com/data-connect/')
	#query = "select id, phenopacket from collections.public_datasets.sample_phenopackets_gecco_phenopackets limit 10"
	query = "select id from collections.public_datasets.sample_phenopackets_gecco_phenopackets where json_extract_scalar(phenopacket, '$.subject.sex') = 'MALE'"

	bqSearchClient = BigQuerySearchClient()
	#query = "select id, phenopacket from collections.public_datasets.sample_phenopackets_gecco_phenopackets limit 10"

	crdcquery = """
		SELECT BioSample_Accession id
		FROM `isbcgc-216220.GECCO_CRC_Susceptibility.Subject_Phenotypes` sp
		JOIN `isbcgc-216220.GECCO_CRC_Susceptibility.Sample_MULTI` sm
			ON sm.dbgap_subject_id = sp.dbgap_subject_id
				AND sex = 'Male'
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

















