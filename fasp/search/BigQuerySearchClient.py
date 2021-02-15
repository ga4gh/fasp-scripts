from google.cloud import bigquery
import pandas as pd

class BigQuerySearchClient:

	def __init__(self ):
		self.bqclient = bigquery.Client()


	def runQuery(self, query, returnType = None):
		query_job = self.bqclient.query(query)  # Send the query
		queryResults = []
		for row in query_job:
			queryResults.append(row)
			
		if returnType == 'dataframe':
			resList = []
			for r in queryResults:
				res = {}
				for k, v in r.items():
					res[k] = v
				resList.append(res)
			df = pd.DataFrame(resList)
			return df
		else:
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
