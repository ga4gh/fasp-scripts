# imports
import sys

from fasp.search  import DiscoverySearchClient



searchClient = DiscoverySearchClient('https://search-presto-public-covid19.prod.dnastack.com/')

queries = ['accession', 'biosample', 'genus', 'species']

res = searchClient.runQuery(query_list=queries, table=searchClient.tables['table42'],
						  results=15)
print(res)