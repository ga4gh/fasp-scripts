# imports
from fasp.search  import DataConnectClient
from fasp.search  import mapping as mp



searchClient = DataConnectClient('https://publisher-data.publisher.dnastack.com/data-connect/', debug=False)

table_name = 'collections.public_datasets.cshcodeathon_organoid_profiling_pc_subject_phenotypes_gru'
map_col = 'sex'
mapping = mp.getMapping(searchClient, table_name, map_col)
print(mapping)

res = searchClient.runOneTableQuery(column_list=['dbgap_subject_id', 'age', 'race', 'sex'],
									table=table_name,
						  			limit=100)
print(res)

res[map_col] = res[map_col].replace(mapping.keys(),mapping.values())

print(res)
