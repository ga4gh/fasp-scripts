#  IMPORTS
import sys
import json
import datetime
import inspect
from fasp.runner.fasp_logger import FASPLogger
from fasp.runner.DemoCredits import Creditor

# These are needed for obtaining notebook name
import os.path
import re
import ipykernel
import requests
from requests.compat import urljoin
from notebook.notebookapp import list_running_servers

class FASPRunner:

	def __init__(self, pipelineLogFile=None, showCredits=None, pauseSecs=0, program=None, test=None):
		"""
		:param pipelineLogFile: path to file to which run submissions will be written. Overrides value in settings
		:param showCredits: whether to show or read credits for different APIs or sources used boolean
		:param pauseSecs: seconds to pause when reading credits number
		:param program: name of program to log, if None will use inspect to determine calling module string
		:param test: set to False to run in test mode where runs are not actually submitted boolean

		"""	
		with open(os.path.expanduser(os.environ['FASP_SETTINGS'])) as json_file:
			self.settings = json.load(json_file)		
		self.searchClient = None
		self.drsClient = None
		self.workClient = None
		
		if program == None:
			# what module are we running this for?
			frm = inspect.stack()[1]
			program = inspect.getsourcefile(frm[0]) 
			
			if program.startswith('<ipython'):
				program = self.get_notebook_name()
				
			print("Running {}".format(program))
			
		if pipelineLogFile == None:
			self.pipelineLogFile = self.settings['PipelineLog']
		else:
			self.pipelineLogFile = pipelineLogFile
		self.pipelineLogger = FASPLogger(self.pipelineLogFile, program)
		self.creditor = Creditor.creditorFactory(self.settings, pauseSecs=pauseSecs)
		
		self.runs = 0
		
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
		creditor.addRun()
		# Step 1 - Discovery
		print("Running query")
		print(query)
		query_job = self.searchClient.runQuery(query)  # Send the query
		creditor.creditClass(self.searchClient)
		# repeat steps 2 and 3 for each row of the query
		runIds = []
		for row in query_job:

			# To do - get the subject/sample name from the query
			runKey = 'subject'
			print("{}={}, drsID={}".format(runKey, row[0], row[1]))
			
		
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
				print('_' * 60)
				runIds.append({runKey:row[0], 'run_id':pipeline_id})
			creditor.creditClass(self.workClient)
			via = 'sh'
			#pipeline_id = 'paste here'

			time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
			if self.live:
				self.pipelineLogger.logRun(time, via, note,  pipeline_id, outfile, str(fileSize),
					self.searchClient, self.drsClient, self.workClient)
				
		creditor.closeRun()
		return runIds
	
	def runDRSIDs(self, idList, note):
		creditor = self.creditor
		creditor.addRun()
		# Step 1 - Discovery
		runIds = []
		for drs_id in idList:

			print("drsID={}".format(drs_id))
			
		
			# Step 2 - Use DRS to get the URL
			objInfo = self.drsClient.getObject(drs_id)
			creditor.creditClass(self.drsClient)
			fileSize = objInfo['size']
			# we've predetermined we want to use the gs copy in this case
			url = self.drsClient.getAccessURL(drs_id)
		
			# Step 3 - Run a pipeline on the file at the drs url
			outfile = "{}.txt".format(drs_id)
			if self.live:
				pipeline_id = self.workClient.runWorkflow(url,  outfile)
				print('workflow submitted, run:{}'.format(pipeline_id))
				print('_' * 60)
				runIds.append({'drs_id':drs_id, 'run_id':pipeline_id})
			creditor.creditClass(self.workClient)
			via = 'sh'
			#pipeline_id = 'paste here'

			time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
			if self.live:
				self.pipelineLogger.logRun(time, via, note,  pipeline_id, outfile, str(fileSize),
					self.searchClient, self.drsClient, self.workClient)
				
		creditor.closeRun()
		return runIds
	
	def rollCredits(self):
		self.creditor.rollCredits()
		
	def getFASPicon(self, filePath=None):
		return self.creditor.getFASPicon(filePath)
	


	def get_notebook_path(self):
	    """
	    Return the full path of the jupyter notebook.
	    """
	    kernel_id = re.search('kernel-(.*).json',
	                          ipykernel.connect.get_connection_file()).group(1)
	    servers = list_running_servers()
	    for ss in servers:
	        response = requests.get(urljoin(ss['url'], 'api/sessions'),
	                                params={'token': ss.get('token', '')})
	        for nn in json.loads(response.text):
	            if nn['kernel']['id'] == kernel_id:
	                relative_path = nn['notebook']['path']
	                return os.path.join(ss['notebook_dir'], relative_path)
	               
	def get_notebook_name(self):
		full_path = self.get_notebook_path()
		return full_path.split("/")[-1]
