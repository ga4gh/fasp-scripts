from google.cloud import bigquery

class BigQuerySearchClient:

	def __init__(self ):
		self.bqclient = bigquery.Client()


	def runQuery(self, query):
	
		query_job = self.bqclient.query(query)  # Send the query
		queryResults = []
		for row in query_job:
			queryResults.append(row)
		return queryResults
			
if __name__ == "__main__":
	myClient = BigQuerySearchClient()

	query = """
     	SELECT 'case_'||associated_entities__case_gdc_id , 'crdc:'||file_id
		FROM `isb-cgc.GDC_metadata.rel24_fileData_active` 
		where data_format = 'BAM' 
		and project_disease_type = 'Breast Invasive Carcinoma'
		limit 3"""
	res = myClient.runQuery(query)
	print (res)
