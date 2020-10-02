#  IMPORTS
import sys, getopt
import json
import datetime
import os
import json
import inspect
from FASPLogger import FASPLogger
from DemoCredits import DemoCredits, Creditor

class FASPRunner:

	def __init__(self, pipelineLogFile, showCredits=None, pauseSecs=1, test=None):
		with open(os.path.expanduser(os.environ['FASP_SETTINGS'])) as json_file:
   			 self.settings = json.load(json_file)		
		self.searchClient = None
		self.drsClient = None
		self.workClient = None
		
		# what module are we running this for?
		frm = inspect.stack()[1]
		program = inspect.getsourcefile(frm[0]) 
		print("Running {}".format(program))
		self.pipelineLogFile = pipelineLogFile
		self.pipelineLogger = FASPLogger(pipelineLogFile, program)
		self.creditor = Creditor.creditorFactory(self.settings, pauseSecs=pauseSecs)
		
		if test != None:
			self.live = not test
		else:
			self.live = not self.settings['test']

    					
	def configure(self, searchClient, drsClient, workClient):
		self.searchClient = searchClient
		self.drsClient = drsClient
		self.workClient = workClient

	def logRun(self, time, via, note, pipeline_id, outfile, fileSize, 
		searcher, finder, computer):
		
		self.pipelineLogger.logRun(time, via, note, pipeline_id, outfile, fileSize, 
		searcher, finder, computer)
					
	def runQuery(self, query, note):
		if None in [self.searchClient, self.drsClient, self.workClient]:
			print ("FASPRunner was not configured")
			sys.exit()
		creditor = self.creditor
		# Step 1 - Discovery
		print("Running query")
		print(query)
		query_job = self.searchClient.runQuery(query)  # Send the query
		creditor.creditClass(self.searchClient)
		# repeat steps 2 and 3 for each row of the query
		for row in query_job:

			print("subject={}, drsID={}".format(row[0], row[1]))
		
			# Step 2 - Use DRS to get the URL
			objInfo = self.drsClient.getObject(row[1])
			creditor.creditClass(self.drsClient)
			fileSize = objInfo['size']
			# we've predetermined we want to use the gs copy in this case
			url = self.drsClient.getAccessURL(row[1])
		
			# Step 3 - Run a pipeline on the file at the drs url
			outfile = "{}.txt".format(row[0])
			if self.live:
				pipeline_id = self.workClient.runWorkflow(url,  outfile)
				print('workflow submitted, run:{}'.format(pipeline_id))
			creditor.creditClass(self.workClient)
			via = 'sh'
			#pipeline_id = 'paste here'

			time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
			if self.live:
				self.pipelineLogger.logRun(time, via, note,  pipeline_id, outfile, str(fileSize),
					self.searchClient, self.drsClient, self.workClient)

		self.pipelineLogger.close()
    
