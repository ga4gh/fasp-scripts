''' Query Search SRA BigQuery tables for 1K Genomes data, access files via SRA DRS ids'''

from fasp.search import BigQuerySearchClient

def main():


	searchClient = BigQuerySearchClient()

	query = """
		SELECT s.sample_name, drs_id, s.acc, assay_type, filename, 
		FROM `nih-sra-datastore.sra.metadata` s, unnest(attributes) att
		join `isbcgc-216220.onek_genomes.sra_drs_files` d on d.acc = s.acc
		where filetype = 'bam' and mapped = 'mapped' and sequencing_type ='exome'
		and att.k = 'population_sam' and att.v = 'JPT' 
		LIMIT 3"""

	searchClient.runQuery(query)
	
if __name__ == "__main__":
	main()
