from fasp.search import BigQuerySearchClient


def main():

	searchClient = BigQuerySearchClient()
	query = """SELECT sra.biosample, sra.acc||'.cram'
		FROM `isbcgc-216220.GECCO_CRC_Susceptibility.Subject_Phenotypes` sp
		join `isbcgc-216220.GECCO_CRC_Susceptibility.Sample_MULTI` sm on
		sm.dbgap_subject_id = sp.dbgap_subject_id
		join `nih-sra-datastore.sra.metadata` sra on sm.BioSample_Accession = sra.biosample
		where AGE between 45 and 55 and sex = 'Female' limit 3"""
	query_job = searchClient.runQuery(query)
	
	# repeat steps 2 and 3 for each row of the query
	for row in query_job:

		print("sample={}, drsID={}".format(row[0], row[1]))
		
if __name__ == "__main__":
	main()
