#  IMPORTS
import sys 

from fasp.search import BigQuerySearchClient

def main(argv):


	searchClient = BigQuerySearchClient()
	query = """
		SELECT submitter_id, read_drs_id
		FROM `isbcgc-216220.onek_genomes.ssd_drs`
		where population = 'BEB'
		LIMIT 1"""

		
	res = searchClient.runQuery(query)
	print (res)
	    
if __name__ == "__main__":
    main(sys.argv[1:])
