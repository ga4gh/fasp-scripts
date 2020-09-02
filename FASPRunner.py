#  IMPORTS
import sys, getopt
import json
import datetime
import os

# a utility 
from FASPLogger import FASPLogger

class FASPRunner:

	def __init__(self, program, searchClient, drsClient, workClient, pipelineLogFile):
		# A log is helpful to keep track of the computes we've submitted
		self.searchClient = searchClient
		self.drsClient = drsClient
		self.workClient = workClient
		self.pipelineLogger = FASPLogger(pipelineLogFile, program)
		
	def runQuery(self, query, note):

		# Step 1 - Discovery
		query_job = self.searchClient.runQuery(query)  # Send the query
	
		# repeat steps 2 and 3 for each row of the query
		for row in query_job:

			print("subject={}, drsID={}".format(row[0], row[1]))
		
			# Step 2 - Use DRS to get the URL
			objInfo = self.drsClient.getObject(row[1])
			fileSize = objInfo['size']
			# we've predetermined we want to use the gs copy in this case
			url = self.drsClient.getAccessURL(row[1])
		
			# Step 3 - Run a pipeline on the file at the drs url
			outfile = "{}.txt".format(row[0])
			pipeline_id = self.workClient.runWorkflow(url,  outfile)
			via = 'sh'
			#pipeline_id = 'paste here'

			time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
			self.pipelineLogger.logRun(time, via, note,  pipeline_id, outfile, str(fileSize),
				self.searchClient, self.drsClient, self.workClient)

		self.pipelineLogger.close()
    
