from google.cloud import bigquery
import pandas as pd
import json

class MappingLibraryClient:

	def __init__(self ):
		self.bqclient = bigquery.Client()
		
		self.dataset_ref = self.bqclient.dataset('metadata')
		table_ref = self.dataset_ref.table('mapping')
		self.map_table = self.bqclient.get_table(table_ref)


	def getNewMapId(self):
		
		query = "SELECT max(map_id) max_id FROM `isbcgc-216220.metadata.mapping` m "
		query_job = self.bqclient.query(query)  # Send the query
		queryResults = []
		for row in query_job:
			next_id = row.max_id + 1
		return next_id
			

	
	def getMappingsForVars(self, varList, returnType = None):	
		
		varString = ''
		for varID in varList:
			if len(varString) == 0:
				varString += '(';
			else:
				varString += ','
			varString += f"'{varID}'"
		varString += ')';
		query = f"""
     		SELECT map_id, m.map_type, m.from_scheme, m.to_scheme, m.to_vocab_id 
			FROM `isbcgc-216220.metadata.mapping` m 
			where m.from_scheme in  {varString} """
		query_job = self.bqclient.query(query)  # Send the query
		queryResults = []
		for row in query_job:
			queryResults.append({'map_id':row.map_id,
								'type':row.map_type,
								'from':row.from_scheme,
								'to':row.to_scheme
								})
			
		if returnType == 'dataframe':
			resList = []
			for r in queryResults:
				res = {}
				for k, v in r.items():
					res[k] = v
					resList.append(res)
					df = pd.DataFrame(resList)
					print( df)
		else:
			return queryResults

	
	def getMappingsForVar(self, varID, returnType = None):
		query = f"""
     	SELECT map_id, m.map_type, m.to_scheme, m.to_vocab_id 
		FROM `isbcgc-216220.metadata.mapping` m 
		where m.from_scheme = '{varID}'"""
		query_job = self.bqclient.query(query)  # Send the query
		queryResults = []
		for row in query_job:
			queryResults.append(row)
			
		if returnType == 'dataframe':
			resList = []
			for r in queryResults:
				res = {}
				for k, v in r.items():
					res[k] = v
				resList.append(res)
			df = pd.DataFrame(resList)
			return df
		else:
			return queryResults
	
	def getJsonMap(self, map_id):
		query = f"""
     	SELECT valueString,	mapto_value_id 
		FROM `isbcgc-216220.metadata.value_map` 
		where map_id = {map_id} """
		query_job = self.bqclient.query(query)  # Send the query
		json_map = {}
		for row in query_job:
			json_map[int(row.valueString)] = row.mapto_value_id	
		return  json_map
	
	def addJsonMap(self, from_scheme, to_scheme, to_vocab_id, json_map):

		map_id = self.getNewMapId()
		map_row = [(map_id, from_scheme, to_scheme, to_vocab_id, u'', u'json_map', u'')]
		errors = self.bqclient.insert_rows(self.map_table, map_row)
		assert errors == []		

		item_table_ref = self.dataset_ref.table('value_map')
		item_table = self.bqclient.get_table(item_table_ref)
		value_rows = []
		for k,v in json_map.items():
			value_rows.append((map_id, k, v))
		errors = self.bqclient.insert_rows(item_table, value_rows)
		assert errors == []
		return 	map_id
		
		
	def addColnameMap(self, from_scheme, to_scheme):

		map_id = self.getNewMapId()
		map_row = [(map_id, from_scheme, to_scheme, u'', u'', u'colname', u'')]
		errors = self.bqclient.insert_rows(self.map_table, map_row)
		assert errors == []
		
		return map_id		

		
if __name__ == "__main__":
	myClient = MappingLibraryClient()

	res = myClient.getMappingsForVar('phv00159572.v4')
	print (res)
