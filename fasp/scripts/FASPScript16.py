''' Compute on ANVIL GTEX files'''
#  IMPORTS
import sys
import json 
import pandas as pd
import datetime

from fasp.runner import FASPRunner

# The implementations we're using
from fasp.loc import sdlDRSClient
from fasp.workflow import GCPLSsamtools


class localSearchClient:
	
	def __init__(self):
		# edit the following for yuor local copy of the manifest file
		dataFile = '/users/forei/fasp/gtex/SRR.breast.cram.txt'
		self.dataTable = pd.read_table(dataFile )
			
	def runQuery(self, query):
		# return the first three records
		# edit this once your ready to run this on all the files
		results = []
		subset = self.dataTable[0:3]
		for index, row in subset.iterrows():
			results.append([row['acc'],row['acc']+'.cram'])
		return  results

def main(argv):

	# edit the following line for where you put your ngc credentials file from dbGaP
	credentials_file = '~/.keys/prj_11218_D17199.ngc'

	faspRunner = FASPRunner(pauseSecs=0)
	settings = faspRunner.settings
	# Step 1 - Discovery
	# query for relevant DRS objects
	searchClient = localSearchClient()
	query_job = searchClient.runQuery('')

	drsClient =  drsClient = sdlDRSClient(credentials_file)

	location = 'projects/{}/locations/{}'.format(settings['GCPProject'], settings['GCPPipelineRegion'])
	mysam = GCPLSsamtools(location, settings['GCPOutputBucket'], debug=True)

	faspRunner = FASPRunner()
	
	# repeat steps 2 and 3 for each row of the query
	for row in query_job:

		print("subject={}, drsID={}".format(row[0], row[1]))
		
		# Step 2 - Use DRS to get the URL
		#objInfo = drsClient.getObject(row[1])
		# for testing
		objInfo = drsClient.getObject(row[1])
		fileSize = objInfo['size']
		print(fileSize)
		# we've predetermined we want to use the gs copy in this case
		#url = drsClient.getAccessURL(row[1], 'gs')
		res = drsClient.getAccessURL(row[1],'gs.us')
		url = res['url']
		print(url)
		# Step 3 - Run a pipeline on the file at the drs url
		outfile = "{}.txt".format(row[0])
		pipeline_id = mysam.runWorkflow(url, outfile)
		print('submitted:{}'.format(pipeline_id))
		
		via = ''
		note = 'Anvil GTEX Test via SDL'

		time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
		faspRunner.logRun(time, via, note,  pipeline_id, outfile, str(fileSize),
			searchClient, drsClient, mysam)

	
if __name__ == "__main__":
	main(sys.argv[1:])


