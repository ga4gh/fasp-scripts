#  IMPORTS
import sys 

from fasp.search import BigQuerySearchClient



def main(argv):

	searchClient = BigQuerySearchClient()

	query = """
     	SELECT 'case_'||associated_entities__case_gdc_id , file_id
		FROM `isb-cgc.GDC_metadata.rel24_fileData_active` 
		where data_format = 'BAM' 
		and project_disease_type = 'Breast Invasive Carcinoma'
		limit 3"""
	
	searchClient.runQuery(query)
	
if __name__ == "__main__":
	main(sys.argv[1:])


	
	

	
	









