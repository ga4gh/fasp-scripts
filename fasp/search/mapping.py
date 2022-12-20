
def getMapping(searchClient, table, column):

    query = "select valueString, maptoValue from collections.public_datasets.md_value_map where table_name = '{}' and column_name='{}'".format(table,column)

    mapping = searchClient.runQuery(query)
    mapDict = {}
    for row in mapping:
        mapDict[row[0]] = row[1]
    return mapDict
