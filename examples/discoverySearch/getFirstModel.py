import requests
import pprint


query = "{\"query\":\"with brca_genes as (select gene_symbol, count(*) as brca_count from search_cloud.brca_exchange.v32 group by gene_symbol) select bg.*, cv.* from brca_genes bg inner join search_cloud.clinvar.allele_gene cv on bg.gene_symbol=cv.symbol limit 1000\"}"

query = "{\"query\":\"select id, population, read_drs_id from thousand_genomes.onek_genomes.ssd_drs limit 1000\"}"

headers = {
  'content-type': 'application/json'
}

next_url = "https://ga4gh-search-adapter-presto-public.prod.dnastack.com/search"

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
			
