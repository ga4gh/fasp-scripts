# imports
from fasp.search  import DataConnectClient



searchClient = DataConnectClient('https://publisher-data.publisher.dnastack.com/data-connect')

res = searchClient.runOneTableQuery(column_list=['accession', 'biosample', 'genus', 'species'],
									table='coronavirus_dnastack_curated.covid_cloud_production.sequences',
						  			limit=15)
print(res)