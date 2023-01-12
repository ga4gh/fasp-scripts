''' Discovery Search - get the first occurrence of the model in returned results.
    The business rule is that the model will be the same throughout the result set.
    The dev team is working on a fix for that
'''
import requests
import pprint

# This query does not appear to be used. However, in case of any uses, please note that the backend has a bug dealing
# with collections.public_datasets.v32. The said bug should be resolved by the end of 2023 Q1.
query = """
	{
		"query": "with brca_genes as (select gene_symbol, count(*) as brca_count from collections.public_datasets.v32 group by gene_symbol) select bg.*, cv.* from brca_genes bg inner join collections.public_datasets.allele_gene cv on bg.gene_symbol=cv.symbol limit 1000"
	}
"""

query = "{\"query\":\"select id, population, read_drs_id from collections.public_datasets.ssd_drs limit 1000\"}"

headers = {
  'content-type': 'application/json'
}

next_url = "https://data.publisher.dnastack.com/data-connect/search"

pageCount = 0
done = False
while next_url != None and not done:
	pageCount += 1
	if pageCount == 1:
		response = requests.request("POST", next_url, headers=headers, data = query)
	else:
		response = requests.request("GET", next_url)
	result = (response.json())
	next_url = result['pagination']['next_page_url']
	if "properties" in result['data_model']:
		pprint.pprint(result['data_model'])
		done = True

