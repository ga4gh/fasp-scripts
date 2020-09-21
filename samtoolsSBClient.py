""" Script to submit a task

        To set your CGC credentials on the API, you will need an authentication token, which you can obtain from
        https://cgc.sbgenomics.com/account/#developer. 
        This code assumes you store your key in ~/.sevenbridges
        

        for questions contact: Ian Fore
"""

import time
import json
import sevenbridges as sbg


class samtoolsSBClient:

	def __init__(self, instance, project):
		#self.outdir = outdir
		self.project_id = project
		config = sbg.Config(profile=instance)
		self.api = sbg.Api(config=config)
		try:
			project = self.api.projects.get(id=self.project_id)
			#print ("Found " + project.name)
		except sbg.SbgError as e:
			print (e.message)

	def getTaskStatus(self, task_id):
		api = self.api

		try:
			task = api.tasks.get(id=task_id)
			return task.status 
		except sbg.NotFound as e:
			return 'Task not found'
		except sbg.SbgError as e:
			print(e.__class__)
			print (e.message)

	def getTaskOutputs(self, task_id, ddir):
		api = self.api

		try:
			task = api.tasks.get(id=task_id)
			if task.status != 'COMPLETED':
				print ('Task status:{}'.format(task.status))
				sys.exit()

			for okey, oitem in task.outputs.items():
				print (okey)
				if oitem.__class__ == sbg.File:
					print(oitem.id)
					print(oitem.name)
				
					drsClient = sbcgcDRSClient('~/.keys/sevenbridges_keys.json')
					drsResponse = drsClient.getObject(oitem.id)
					print(drsResponse) 
					drsURL = drsClient.getAccessURL(oitem.id, 's3')
					dPath = os.path.expanduser(ddir+oitem.name)
					if ddir != None:
						download(drsURL, dPath)
				
				else:
					print(oitem)

		except sbg.NotFound as e:
			print('Task not found')
		except sbg.SbgError as e:
			print(e.__class__)
			print (e.message)


	def runWorkflow(self, bamURL, outfile):
		api = self.api
		# Task name in my project
		name = 'samtools_test'

		# App I want to use to run a task
		app = 'forei/gecco/samtools-stats-1-8-url'

		# Inputs
		inputs = {}
		
		inputs['alignment_file_url'] = bamURL
		inputs['output_file_path'] = outfile
		# static for now
		inputs['reference_file'] = api.files.get('5bad6c83e4b0abc138917143')

		task = api.tasks.create(name=name, project=self.project_id, app=app, inputs=inputs, run=True)
		return task.id


if __name__ == "__main__":
	sbApp = 'cgc'	# NCI Cancer Genomics Cloud
	project = 'forei/gecco'
	
	myClient = samtoolsSBClient(sbApp, project)

	drsurl = "s3://sddp-phs001554/117438.recal.cram"
	task = myClient.runWorkflow(drsurl, '117438.recal_stats.txt')
	print('task.id: {}'.format(task))


