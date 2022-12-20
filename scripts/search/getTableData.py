import requests
import pprint

# FIXME https://www.pivotaltracker.com/story/show/184043487
query = "{\"query\":\"with brca_genes as (select gene_symbol, count(*) as brca_count from collections.public_datasets.v32 group by gene_symbol) select bg.*, cv.* from brca_genes bg inner join collections.public_datasets.allele_gene cv on bg.gene_symbol=cv.symbol limit 1000\"}"
headers = {
  'content-type': 'application/json'
}

next_url = "https://publisher-data.publisher.dnastack.com/data-connect/table/search_cloud.clinvar.allele_gene/data"

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

