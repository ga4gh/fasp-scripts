import requests
import pprint

# Please note that the backend has a bug dealing with collections.public_datasets.brca_exchange_v32. The said bug should be resolved by the end of 2023 Q1.
query = "{\"query\":\"with brca_genes as (select gene_symbol, count(*) as brca_count from collections.public_datasets.brca_exchange_v32 group by gene_symbol) select bg.*, cv.* from brca_genes bg inner join collections.public_datasets.clinvar_allele_gene cv on bg.gene_symbol=cv.symbol limit 1000\"}"
headers = {
  'content-type': 'application/json'
}

next_url = "https://publisher-data.publisher.dnastack.com/data-connect/table/collections.public_datasets.clinvar_allele_gene/data"

pageCount = 0
while next_url != None :
	pageCount += 1
	print ("____Page{}_______________".format(pageCount))
	response = requests.request("GET", next_url)
	result = (response.json())
	pprint.pprint(result)
	next_url = result['pagination']['next_page_url']

#	print ("has {} data rows".format(len(result['data'])))
# 	if "properties" in result['data_model']:
# 		dm = result['data_model']
# 		print ("has {} data model properties".format(len(dm['properties'])))
# 		for prop in dm['properties'].keys():
# 			print (prop)
# 		if last_model == dm:
# 			print ("model is same as on previous page")
# 		else:
# 			print ("model is different than previous page")
# 		last_model = dm

