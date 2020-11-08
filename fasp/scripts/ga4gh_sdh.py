# imports
from fasp.search  import DiscoverySearchClient



searchClient = DiscoverySearchClient('https://search-presto-public-covid19.prod.dnastack.com')

res = searchClient.runOneTableQuery(column_list=['accession', 'biosample', 'genus', 'species'], 
									table='coronavirus_dnastack_curated.covid_cloud_production.sequences',
						  			limit=15)
print(res)