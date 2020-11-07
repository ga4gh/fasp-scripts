''' Query Search SRA tables for 1K Genomes data, access files via SRA DRS ids'''
#  IMPORTS
import sys 

from fasp.search import DiscoverySearchClient

def main(argv):


	searchClient = DiscoverySearchClient('https://ga4gh-search-adapter-presto-public.prod.dnastack.com', debug=False)

	query = "SELECT s.su_submitter_id, drs_id FROM thousand_genomes.onek_genomes.ssd_drs s join thousand_genomes.onek_genomes.sra_drs_files f on f.sample_name = s.su_submitter_id where filetype = 'bam' and mapped = 'mapped' and sequencing_type ='exome' and  population = 'JPT' LIMIT 3"

		
	searchClient.runQuery(query)
	    
if __name__ == "__main__":
    main(sys.argv[1:])
