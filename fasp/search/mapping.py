
def getMapping(searchClient, table, column):
    
    query = "select valueString, maptoValue from search_cloud.cshcodeathon.md_value_map where table_name = '{}' and column_name='{}'".format(table,column)
    
    mapping = searchClient.run_query(query)
    mapDict = {}
    for row in mapping:
        mapDict[row[0]] = row[1]
    return mapDict
