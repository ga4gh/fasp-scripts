import json

class Gen3ManifestClient:
	''' class to simulate a GA4GH Search Server from a local file'''	
	def __init__(self, filepath):
		# edit the following for your local copy of the manifest file
		with open(filepath) as f:
			self.data = json.load(f)
			
	def runQuery(self, limit):
		''' expects an integer as query to limit the rows from the file to return'''
		# return the first limit records
		results = []
		for f in self.data[0:limit]:
			results.append([f['file_name'],f['object_id']])
		return  results