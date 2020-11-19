#  IMPORTS
import sys
from fasp.search import BigQuerySearchClient


def main(argv):

	
	searchClient = BigQuerySearchClient()

	# TCGA Query - CRDC
	crdcquery = """
     	SELECT 'case_'||associated_entities__case_gdc_id , 'crdc:'||file_id
		FROM `isb-cgc.GDC_metadata.rel24_fileData_active` 
		where data_format = 'BAM' 
		and project_disease_type = 'Breast Invasive Carcinoma'
		limit 3"""
	
	#COPD query - Topmed	
	bdcquery = """
  		SELECT SUBJECT_ID, 'bdc:'||read_drs_id
  		FROM `isbcgc-216220.COPDGene.phenotype_drs`
      	where Weight_KG between 92.5 and 93.0
      	LIMIT 3"""
  		
	results = searchClient.runQuery(crdcquery)  # Send the query
	results += searchClient.runQuery(bdcquery)  

	# repeat steps 2 and 3 for each row of the query
	for row in results:

		print("subject={}, drsID={}".format(row[0], row[1]))
		    
if __name__ == "__main__":
    main(sys.argv[1:])
    


	
	

	
	









