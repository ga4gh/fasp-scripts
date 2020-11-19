# imports
from fasp.search  import DiscoverySearchClient

def getMapping(searchClient, table, column):
	
	query = """select valueString, maptoValue  
	from search_cloud.cshcodeathon.md_value_map 
	where table_name = '{}' and column_name='{}'".format(table,column)"""
	
	mapping = searchClient.runQuery(query)
	mapDict = {}
	for row in mapping:
		mapDict[row[0]] = row[1]
	return mapDict
	

searchClient = DiscoverySearchClient('https://ga4gh-search-adapter-presto-public.prod.dnastack.com', debug=False)

table_name = 'search_cloud.cshcodeathon.organoid_profiling_pc_subject_phenotypes_gru'
map_col = 'sex'
mapping = getMapping(searchClient, table_name, map_col)
print(mapping)

res = searchClient.runOneTableQuery(column_list=['dbgap_subject_id', 'age', 'race', 'sex'], 
									table=table_name,
						  			limit=100)
print(res)

res[map_col] = res[map_col].replace(mapping.keys(),mapping.values())

print(res)
